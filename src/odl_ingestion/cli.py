import typer
import os
from pathlib import Path
from typing import Optional
from .catalog.loader import CatalogLoader
from .connectors.weather.meteocat import MeteocatConnector
from .writers.local import LocalWriter
from .validation.records import validate_record

app = typer.Typer(help="Open Data Lakehouse Ingestion CLI")
datasets_app = typer.Typer(help="Dataset catalog management")
app.add_typer(datasets_app, name="datasets")

@app.command()
def version() -> None:
    """Show the version of the ingestion tool."""
    typer.echo("odl-ingestion version 0.1.0")

@datasets_app.command("list")
def list_datasets(
    catalog_path: str = typer.Option("../datasets-catalog", "--catalog-path", help="Path to the dataset catalog repository")
) -> None:
    """List available datasets from the catalog."""
    loader = CatalogLoader(catalog_path)
    datasets = loader.list_datasets()
    if not datasets:
        typer.echo("No datasets found in catalog.")
        return
    
    for ds in datasets:
        typer.echo(f"- {ds.id}: {ds.name} ({ds.status})")

@datasets_app.command("show")
def show_dataset(
    dataset_id: str,
    catalog_path: str = typer.Option("../datasets-catalog", "--catalog-path", help="Path to the dataset catalog repository")
) -> None:
    """Show details of a specific dataset."""
    loader = CatalogLoader(catalog_path)
    try:
        ds = loader.get_dataset(dataset_id)
        typer.echo(f"ID: {ds.id}")
        typer.echo(f"Name: {ds.name}")
        typer.echo(f"Description: {ds.description}")
        typer.echo(f"Status: {ds.status}")
        typer.echo(f"Category: {ds.category}")
        typer.echo(f"Format: {ds.format}")
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

@app.command()
def ingest(
    dataset: str = typer.Option(..., "--dataset", help="Dataset ID to ingest"),
    catalog_path: str = typer.Option("../datasets-catalog", "--catalog-path", help="Path to the dataset catalog repository"),
    target: str = typer.Option("local", "--target", help="Target writer type"),
    output_dir: str = typer.Option("./data", "--output-dir", help="Output directory for local target"),
    mode: str = typer.Option("sample", "--mode", help="Ingestion mode (sample or real)"),
    meteocat_resource: str = typer.Option("stations-metadata", "--meteocat-resource", help="Meteocat resource to ingest (stations-metadata, variables-metadata, measured-variable)"),
    station_status: str = typer.Option("all", "--station-status", help="Filter by station status"),
    metadata_date: Optional[str] = typer.Option(None, "--metadata-date", help="Metadata date (YYYY-MM-DD)"),
    variable_code: Optional[str] = typer.Option(None, "--variable-code", help="Variable code for measured data"),
    year: Optional[int] = typer.Option(None, "--year", help="Year for measured data"),
    month: Optional[int] = typer.Option(None, "--month", help="Month for measured data"),
    day: Optional[int] = typer.Option(None, "--day", help="Day for measured data"),
    station_code: Optional[str] = typer.Option(None, "--station-code", help="Station code for measured data")
) -> None:
    """Run ingestion for a dataset."""
    # Load catalog to verify dataset exists
    if not Path(catalog_path).exists():
        typer.echo(f"Error: Catalog path '{catalog_path}' does not exist.", err=True)
        raise typer.Exit(code=1)

    loader = CatalogLoader(catalog_path)
    
    try:
        ds = loader.get_dataset(dataset)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    if ds.status not in ["selected", "candidate"]:
        typer.echo(f"Error: Dataset '{dataset}' has status '{ds.status}'. Ingestion is only allowed for 'selected' or 'candidate' datasets.", err=True)
        raise typer.Exit(code=1)

    if dataset == "meteocat-weather":
        connector = MeteocatConnector()
        
        if mode == "sample":
            typer.echo(f"Extracting sample from {dataset}...")
            data = connector.extract_sample()
            filename = "sample.json"
        elif mode == "real":
            api_key = os.getenv("METEOCAT_API_KEY")
            if not api_key:
                typer.echo("Error: METEOCAT_API_KEY environment variable is required for real mode.", err=True)
                raise typer.Exit(code=1)
            
            if meteocat_resource == "stations-metadata":
                typer.echo(f"Extracting {meteocat_resource} from {dataset} (real mode)...")
                data = connector.extract_station_metadata(
                    api_key=api_key,
                    station_status=station_status,
                    metadata_date=metadata_date
                )
                filename = "stations-metadata.json"
            elif meteocat_resource == "variables-metadata":
                typer.echo(f"Extracting {meteocat_resource} from {dataset} (real mode)...")
                data = connector.extract_variables_metadata(
                    api_key=api_key
                )
                filename = "variables-metadata.json"
            elif meteocat_resource == "measured-variable":
                if not all([variable_code, year, month, day]):
                    typer.echo("Error: --variable-code, --year, --month and --day are required for measured-variable resource.", err=True)
                    raise typer.Exit(code=1)
                
                typer.echo(f"Extracting {meteocat_resource} from {dataset} (real mode)...")
                # We know they are not None because of the check above, but for type checker:
                assert variable_code is not None
                assert year is not None
                assert month is not None
                assert day is not None

                data = connector.extract_measured_variable(
                    api_key=api_key,
                    variable_code=variable_code,
                    year=year,
                    month=month,
                    day=day,
                    station_code=station_code
                )
                filename = "measured-variable.json"
            else:
                typer.echo(f"Error: Meteocat resource '{meteocat_resource}' is not supported.", err=True)
                raise typer.Exit(code=1)
        else:
            typer.echo(f"Error: Mode '{mode}' is not supported.", err=True)
            raise typer.Exit(code=1)
        
        # Validation is optional for now, but we keep it for sample
        # For real data, we might want to be more flexible or have a different validator
        if mode == "sample" and not validate_record(data):
             typer.echo("Error: Sample data validation failed.", err=True)
             raise typer.Exit(code=1)

        if target == "local":
            writer = LocalWriter()
            # We need to update LocalWriter to accept filename or handle it better
            output_path = writer.write(data, dataset, output_dir, filename=filename)
            typer.echo(f"Successfully ingested {dataset}.")
            typer.echo(f"Output written to: {output_path}")
        else:
            typer.echo(f"Error: Target '{target}' not supported yet.", err=True)
            raise typer.Exit(code=1)
    else:
        typer.echo(f"Ingestion for dataset '{dataset}' is not implemented yet.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

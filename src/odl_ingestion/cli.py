import typer
from pathlib import Path
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
    output_dir: str = typer.Option("./data", "--output-dir", help="Output directory for local target")
) -> None:
    """Run ingestion for a dataset (placeholder)."""
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
        typer.echo(f"Extracting sample from {dataset}...")
        sample_data = connector.extract_sample()
        
        if not validate_record(sample_data):
             typer.echo("Error: Sample data validation failed.", err=True)
             raise typer.Exit(code=1)

        if target == "local":
            writer = LocalWriter()
            output_path = writer.write(sample_data, dataset, output_dir)
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

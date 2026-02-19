import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from database import Database
from models import Customer

app = typer.Typer(help="A simple CLI tool for small businesses to manage customer contacts")
console = Console()
db = Database()

@app.command()
def add(
    name: str = typer.Option(..., prompt=True, help="Customer name"),
    company: str = typer.Option("", prompt=True, help="Company name"),
    phone: str = typer.Option("", prompt=True, help="Phone number"),
    email: str = typer.Option("", prompt=True, help="Email address"),
    notes: str = typer.Option("", prompt=True, help="Additional notes")
):
    """Add a new customer"""
    customer = Customer(name=name, company=company, phone=phone, email=email, notes=notes)
    customer_id = db.add_customer(customer)
    console.print(f"[green]Customer added successfully with ID: {customer_id}[/green]")

@app.command()
def edit(customer_id: int = typer.Argument(..., help="Customer ID to edit")):
    """Edit an existing customer"""
    customer = db.get_customer(customer_id)
    if not customer:
        console.print(f"[red]Customer with ID {customer_id} not found[/red]")
        return
    
    console.print(f"Editing customer: {customer.name}")
    name = typer.prompt("Name", default=customer.name)
    company = typer.prompt("Company", default=customer.company)
    phone = typer.prompt("Phone", default=customer.phone)
    email = typer.prompt("Email", default=customer.email)
    notes = typer.prompt("Notes", default=customer.notes)
    
    customer.name = name
    customer.company = company
    customer.phone = phone
    customer.email = email
    customer.notes = notes
    
    db.update_customer(customer)
    console.print("[green]Customer updated successfully[/green]")

@app.command()
def list():
    """List all customers"""
    customers = db.get_all_customers()
    if not customers:
        console.print("[yellow]No customers found[/yellow]")
        return
    
    table = Table(title="Customer List")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Company", style="blue")
    table.add_column("Phone")
    table.add_column("Email")
    table.add_column("Remind Date", style="yellow")
    
    for customer in customers:
        remind_date = customer.remind_date if customer.remind_date else ""
        table.add_row(
            str(customer.id),
            customer.name,
            customer.company,
            customer.phone,
            customer.email,
            remind_date
        )
    
    console.print(table)

@app.command()
def search(query: str = typer.Argument(..., help="Search query for name or company")):
    """Search customers by name or company"""
    customers = db.search_customers(query)
    if not customers:
        console.print(f"[yellow]No customers found matching '{query}'[/yellow]")
        return
    
    table = Table(title=f"Search Results for '{query}'")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Company", style="blue")
    table.add_column("Phone")
    table.add_column("Email")
    
    for customer in customers:
        table.add_row(
            str(customer.id),
            customer.name,
            customer.company,
            customer.phone,
            customer.email
        )
    
    console.print(table)

@app.command()
def remind(
    customer_id: int = typer.Argument(..., help="Customer ID"),
    date: str = typer.Argument(..., help="Remind date (YYYY-MM-DD)")
):
    """Set a reminder date for updating customer information"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        console.print("[red]Invalid date format. Use YYYY-MM-DD[/red]")
        return
    
    customer = db.get_customer(customer_id)
    if not customer:
        console.print(f"[red]Customer with ID {customer_id} not found[/red]")
        return
    
    db.set_remind_date(customer_id, date)
    console.print(f"[green]Reminder set for {customer.name} on {date}[/green]")

@app.command()
def reminders():
    """Show customers with upcoming reminders"""
    customers = db.get_customers_with_reminders()
    if not customers:
        console.print("[yellow]No reminders set[/yellow]")
        return
    
    table = Table(title="Upcoming Reminders")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Company", style="blue")
    table.add_column("Remind Date", style="yellow")
    
    today = datetime.now().strftime("%Y-%m-%d")
    for customer in customers:
        style = "red" if customer.remind_date <= today else ""
        table.add_row(
            str(customer.id),
            customer.name,
            customer.company,
            customer.remind_date,
            style=style
        )
    
    console.print(table)

if __name__ == "__main__":
    app()

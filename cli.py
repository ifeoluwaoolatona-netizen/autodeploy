import typer, subprocess, tempfile, shutil
from pathlib import Path
from repo_analyzer import improved_sniff
from planner import plan_deployment
from renderer import render_templates

app = typer.Typer()

@app.command()
def deploy(desc: str, repo: str):
    """Deploy an app given natural language description + repo link"""
    typer.echo(f"[LOG] Starting deployment: {desc}, repo={repo}")
    tmpdir = Path(tempfile.mkdtemp())
    subprocess.run(["git", "clone", repo, str(tmpdir)], check=True)
    
    info = improved_sniff(tmpdir)
    typer.echo(f"[LOG] Repo analysis: {info}")
    
    plan = plan_deployment(desc, info)
    typer.echo(f"[LOG] Planner chose: {plan}")
    
    outdir = Path("deploy_out")
    shutil.rmtree(outdir, ignore_errors=True)
    outdir.mkdir()
    
    render_templates(plan, info, outdir)
    typer.echo("[LOG] Templates rendered.")
    
    subprocess.run(["terraform", "init"], cwd=outdir, check=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=outdir, check=True)
    typer.echo("[LOG] Deployment finished.")

@app.command()
def destroy():
    """Tear down deployed infra"""
    outdir = Path("deploy_out")
    subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=outdir, check=True)

if __name__ == "__main__":
    app()

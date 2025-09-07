from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import shutil

def render_templates(plan, info, outdir):
    env = Environment(loader=FileSystemLoader("templates"))
    
    if plan["strategy"]=="ec2":
        main_tf = env.get_template("ec2_main.tf.j2").render(port=plan["port"])
        (outdir/"main.tf").write_text(main_tf)
        user_data = env.get_template("user_data_flask.sh.j2").render(
            start_cmd=info["start_cmd"] or "python app.py"
        )
        (outdir/"user_data.sh").write_text(user_data)
    elif plan["strategy"]=="ecs_fargate":
        main_tf = env.get_template("ecs_main.tf.j2").render(port=plan["port"])
        (outdir/"main.tf").write_text(main_tf)

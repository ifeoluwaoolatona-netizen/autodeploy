def plan_deployment(desc, info):
    if info["container"]:
        return {"strategy":"ecs_fargate","port":info["port"] or 80}
    if info["app_type"] in ("flask","django","node"):
        return {"strategy":"ec2","port":info["port"] or 80}
    return {"strategy":"ec2","port":80}

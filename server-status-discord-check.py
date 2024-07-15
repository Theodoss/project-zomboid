import json
import requests
import subprocess

# 获取当前的外部IP地址（从GCP元数据服务器）
def get_current_ip():
    response = requests.get("http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip",
                            headers={"Metadata-Flavor": "Google"})
    return response.text

# 更新 DiscordGSM 的 config.json 文件
def update_config_file(new_ip):
    config_path = "/path/to/your/config.json"  # 修改为您的config.json文件路径

    with open(config_path, "r") as file:
        config = json.load(file)

    # 假设我们只需要更新第一个服务器的IP
    config['servers'][0]['host'] = new_ip

    with open(config_path, "w") as file:
        json.dump(config, file, indent=4)

    print(f"Updated server IP to: {new_ip}")

# 重新启动 Docker 容器
def restart_docker_container():
    container_name = "discord-game-server-monitor"
    subprocess.run(["docker", "restart", container_name])
    print(f"Restarted Docker container: {container_name}")

def main():
    new_ip = get_current_ip()
    update_config_file(new_ip)
    restart_docker_container()

if __name__ == "__main__":
    main()

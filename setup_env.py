import os
import subprocess
import sys
import stat


def create_virtualenv(env_name):
    # Create virtual environment
    subprocess.check_call([sys.executable, "-m", "venv", env_name])


def set_executable_permissions(file_path):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)


def install_requirements(env_name):
    # Activate the virtual environment
    activate_script = os.path.join(env_name, "bin", "activate")
    pip_path = os.path.join(env_name, "bin", "pip")
    set_executable_permissions(activate_script)

    # Install requirements
    subprocess.check_call([pip_path,
                          "install", "-r", "requirements.txt"])


if __name__ == "__main__":
    env_name = ".venv"

    if not os.path.exists("requirements.txt"):
        print(
            "requirements.txt not found. Please create one with the necessary dependencies.")
        sys.exit(1)

    create_virtualenv(env_name)
    install_requirements(env_name)

    print(f"""Virtual environment '{
          env_name}' is set up and dependencies are installed.""")
    print(f"To activate the virtual environment, run:")
    print(f"source ./{env_name}/bin/activate")

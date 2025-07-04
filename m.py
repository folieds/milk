import os, subprocess, sys, time
from dotenv import load_dotenv

load_dotenv()

CLONE_DIR = "cloned_bots"
os.makedirs(CLONE_DIR, exist_ok=True)
MAX_BOTS = 10
processes = []

def clone_repo(repo_url, bot_number):
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    local_path = os.path.join(CLONE_DIR, f"bot{bot_number}_{repo_name}")
    if not os.path.exists(local_path):
        print(f"⬇️ Cloning BOT{bot_number} from {repo_url} ...")
        try:
            subprocess.check_call(["git", "clone", repo_url, local_path])
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone BOT{bot_number}: {e}")
            return None
    return local_path

for i in range(1, MAX_BOTS + 1):
    path = os.getenv(f"BOT{i}_PATH")
    cmd = os.getenv(f"BOT{i}_CMD")

    if not path or not cmd:
        continue

    local_path = clone_repo(path, i) if path.startswith("http") else path
    if not local_path:
        continue

    cmd_list = cmd.strip().split()
    print(f"🚀 Starting BOT{i} in {local_path} with {cmd_list}")
    try:
        proc = subprocess.Popen(cmd_list, cwd=local_path)
        processes.append(proc)
    except Exception as e:
        print(f"❌ Failed to start BOT{i}: {e}")

if not processes:
    print("⚠️ No bots started. Sleeping forever to keep container healthy.")
    while True:
        time.sleep(3600)

print(f"✅ Started {len(processes)} bots. Watching...")

try:
    while True:
        for i, proc in enumerate(processes):
            if proc.poll() is not None:
                print(f"🔁 Restarting BOT{i+1}...")
                # restart logic: not implemented yet, just exit
                sys.exit(1)
        time.sleep(10)
except KeyboardInterrupt:
    print("🛑 Stopping all bots...")
    for proc in processes:
        proc.terminate()
      

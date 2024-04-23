import os
import json
import argparse
from datetime import datetime
from decision.Model import *
from run import run
from Env.Env import Env
from tqdm import tqdm
# 创建ArgumentParser对象
parser = argparse.ArgumentParser(
    description='Continue evaluation if a folder name is provided.')
parser.add_argument('--folder_name', type=str,
                    help='Name of the folder to continue evaluation.')
# parser.add_argument('--llm_model_path', type=str, required=True, help='Path to the LLM model.')
# parser.add_argument('--llm_port', type=int, required=True, help='Port number for the LLM.')

args = parser.parse_args()

# 检查是否提供了文件夹名
if args.folder_name:
    # 指定的文件夹路径
    folder_path = args.folder_name
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(
            f"Folder {folder_path} does not exist. Starting a new evaluation.")
        # 创建一个基于当前日期的文件夹来存放结果
        folder_path = datetime.datetime.now().strftime('%Y-%m-%d')
        os.makedirs(folder_path)
else:
    # 创建一个基于当前日期的文件夹来存放结果
    folder_path = datetime.datetime.now().strftime('%Y-%m-%d')
    os.makedirs(folder_path, exist_ok=True)

# 在指定的文件夹内创建或查找任务总结文件
summary_file_path = os.path.join(folder_path, 'task_summary.json')

# 读取总结文件以确定下一个应该执行的任务
completed_tasks = set()
if os.path.exists(summary_file_path):
    with open(summary_file_path, 'r') as summary_file:
        for line in summary_file:
            task_result = json.loads(line)
            completed_tasks.add(next(iter(task_result)))
llm_model_path = ""
llm_port = ""
# llm = Modal(args.llm_model_path, args.llm_port)
llm = Modal(llm_model_path, llm_port)

# 读取数据并执行任务
with open("evaluate/WebVoyager_data.jsonl", "r") as f:
    data = [json.loads(x.strip()) for x in f]
with tqdm(total=len(data),desc="Processing") as pbar:
    for task_data in data:
        task_id = task_data["id"]
        # 跳过已完成的任务
        if task_id in completed_tasks:
            continue

        # 执行任务...
        # 假设run函数返回任务结果
        try:
            env = Env(task_data["web"], headless=True)
            res = run(llm, env, task_data["ques"])

        except Exception as e:
            res = e
        finally:
            # 更新任务结果到总结文件
            with open(summary_file_path, 'a') as summary_file:
                json.dump({task_id: res}, summary_file)
                summary_file.write('\n')
            pbar.update(1)

# 注意：这里假设每个任务在"data.jsonl"中有一个唯一的"id"字段，用于标识任务。
# run函数需要相应地实现以返回任务的结果。

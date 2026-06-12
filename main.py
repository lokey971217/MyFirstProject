"""
猜年龄游戏
功能：玩家猜测随机生成的年龄，游戏记录每次的猜测次数和成绩
"""

import random
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class GuessAgeGame:
    """猜年龄游戏主类"""

    def __init__(self, min_age: int = 1, max_age: int = 100, max_attempts: int = 10):
        """
        初始化游戏

        Args:
            min_age: 最小年龄范围
            max_age: 最大年龄范围
            max_attempts: 最大猜测次数
        """
        self.min_age = min_age
        self.max_age = max_age
        self.max_attempts = max_attempts
        self.target_age = None
        self.attempts = 0
        self.game_history = []
        self.history_file = "game_history.json"
        self.load_history()

    def start_new_game(self) -> None:
        """开始新游戏，重置状态"""
        self.target_age = random.randint(self.min_age, self.max_age)
        self.attempts = 0
        print(f"\n{'=' * 50}")
        print(f"🎮 猜年龄游戏开始！")
        print(f"📌 年龄范围: {self.min_age} - {self.max_age} 岁")
        print(f"📌 最多猜测次数: {self.max_attempts} 次")
        print(f"{'=' * 50}\n")

    def make_guess(self, guess: int) -> Dict[str, any]:
        """
        处理用户猜测

        Args:
            guess: 用户猜测的年龄

        Returns:
            包含猜测结果的字典
        """
        self.attempts += 1
        remaining = self.max_attempts - self.attempts

        if guess < self.target_age:
            message = f"📈 太小了！{guess}岁太年轻了"
            is_correct = False
        elif guess > self.target_age:
            message = f"📉 太大了！{guess}岁太老了"
            is_correct = False
        else:
            message = f"🎉 恭喜！猜对了！就是 {self.target_age} 岁！"
            message += f"\n✨ 你用了 {self.attempts} 次猜测"
            is_correct = True

        if remaining > 0 and not is_correct:
            message += f" (还剩 {remaining} 次机会)"

        return {
            "guess": guess,
            "attempts": self.attempts,
            "is_correct": is_correct,
            "message": message,
            "remaining": remaining
        }

    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.attempts >= self.max_attempts

    def save_game_result(self, player_name: str, won: bool) -> None:
        """
        保存游戏结果到历史记录

        Args:
            player_name: 玩家姓名
            won: 是否获胜
        """
        result = {
            "player_name": player_name,
            "target_age": self.target_age,
            "attempts_used": self.attempts if won else self.max_attempts,
            "won": won,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "max_attempts": self.max_attempts,
            "age_range": f"{self.min_age}-{self.max_age}"
        }
        self.game_history.append(result)
        self.save_history()

    def save_history(self) -> None:
        """保存游戏历史到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存历史记录失败: {e}")

    def load_history(self) -> None:
        """从文件加载游戏历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.game_history = json.load(f)
            except Exception as e:
                print(f"⚠️ 加载历史记录失败: {e}")
                self.game_history = []
        else:
            self.game_history = []

    def show_statistics(self) -> None:
        """显示游戏统计数据"""
        if not self.game_history:
            print("\n📊 暂无游戏记录")
            return

        total_games = len(self.game_history)
        won_games = sum(1 for game in self.game_history if game["won"])
        win_rate = (won_games / total_games) * 100 if total_games > 0 else 0

        # 计算平均猜测次数（只计算获胜的游戏）
        attempts_won = [game["attempts_used"] for game in self.game_history if game["won"]]
        avg_attempts = sum(attempts_won) / len(attempts_won) if attempts_won else 0

        # 找出最佳成绩（最少猜测次数）
        best_score = min(attempts_won) if attempts_won else None

        print(f"\n{'=' * 50}")
        print(f"📊 游戏统计")
        print(f"{'=' * 50}")
        print(f"总游戏次数: {total_games}")
        print(f"获胜次数: {won_games}")
        print(f"胜率: {win_rate:.1f}%")
        print(f"平均猜测次数(获胜): {avg_attempts:.1f}")
        if best_score:
            print(f"最佳成绩: {best_score} 次猜测")
        print(f"{'=' * 50}")

    def show_history(self, limit: int = 10) -> None:
        """
        显示最近的游戏历史

        Args:
            limit: 显示最近多少条记录
        """
        if not self.game_history:
            print("\n📜 暂无游戏历史记录")
            return

        print(f"\n{'=' * 60}")
        print(f"📜 最近游戏历史（显示最近{limit}条）")
        print(f"{'=' * 60}")

        for i, game in enumerate(reversed(self.game_history[-limit:]), 1):
            result = "✅ 获胜" if game["won"] else "❌ 失败"
            print(f"{i}. 玩家: {game['player_name']} | "
                  f"目标年龄: {game['target_age']} | "
                  f"猜测次数: {game['attempts_used']} | "
                  f"结果: {result} | "
                  f"日期: {game['date']}")
        print(f"{'=' * 60}")


def get_player_name() -> str:
    """获取玩家姓名"""
    while True:
        name = input("请输入你的名字: ").strip()
        if name:
            return name
        print("⚠️ 姓名不能为空，请重新输入！")


def get_valid_guess(game: GuessAgeGame) -> int:
    """
    获取有效的用户猜测输入

    Args:
        game: 游戏实例

    Returns:
        有效的猜测数字
    """
    while True:
        try:
            guess = int(input(f"🔢 请输入你的猜测 ({game.min_age}-{game.max_age}): "))
            if game.min_age <= guess <= game.max_age:
                return guess
            else:
                print(f"⚠️ 请输入 {game.min_age} 到 {game.max_age} 之间的数字！")
        except ValueError:
            print("⚠️ 请输入有效的数字！")


def play_game():
    """主游戏循环"""
    game = GuessAgeGame()
    player_name = get_player_name()

    while True:
        game.start_new_game()

        game_won = False

        while not game.is_game_over() and not game_won:
            guess = get_valid_guess(game)
            result = game.make_guess(guess)
            print(f"\n{result['message']}\n")

            if result["is_correct"]:
                game_won = True
                game.save_game_result(player_name, True)
            elif game.is_game_over():
                print(f"💔 很遗憾，机会用完了！正确答案是 {game.target_age} 岁")
                game.save_game_result(player_name, False)

        # 显示本轮结果统计
        print(f"\n本轮{'获胜' if game_won else '失败'}！")
        print(f"本轮使用猜测次数: {game.attempts if game_won else game.max_attempts}")

        # 显示全局统计
        game.show_statistics()

        # 询问是否继续
        while True:
            play_again = input("\n🔄 是否继续游戏？(y/n): ").strip().lower()
            if play_again in ['y', 'yes', '是']:
                break
            elif play_again in ['n', 'no', '否']:
                # 显示历史记录后退出
                game.show_history()
                print(f"\n👋 感谢 {player_name} 玩游戏，再见！")
                return
            else:
                print("⚠️ 请输入 y 或 n")


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\n👋 游戏被中断，再见！")
    except Exception as e:
        print(f"\n❌ 游戏出现错误: {e}")

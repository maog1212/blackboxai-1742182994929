#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
左右互搏术练习程序
基于金庸武侠小说中的"左右互搏术"概念
"""

import random
import time
import os
from typing import Dict, List, Tuple

# ==================== 招式系统 ====================

class Move:
    """武功招式类"""
    def __init__(self, name: str, move_type: str, power: int, description: str):
        self.name = name
        self.move_type = move_type  # 拳、掌、指、剑、内功
        self.power = power
        self.description = description

    def __str__(self):
        return f"「{self.name}」({self.move_type})"


# 定义所有招式
MOVES = {
    "亢龙有悔": Move("亢龙有悔", "掌", 95, "降龙十八掌第一式，掌力雄浑"),
    "飞龙在天": Move("飞龙在天", "掌", 90, "降龙十八掌第二式，气势磅礴"),
    "空明拳": Move("空明拳", "拳", 85, "古墓派绝学，以柔克刚"),
    "玉女素心剑": Move("玉女素心剑", "剑", 88, "古墓派剑法，清雅脱俗"),
    "一阳指": Move("一阳指", "指", 92, "大理段氏绝学，指力惊人"),
    "六脉神剑": Move("六脉神剑", "指", 98, "大理段氏最高武学"),
    "太极拳": Move("太极拳", "拳", 80, "以柔克刚，四两拨千斤"),
    "黯然销魂掌": Move("黯然销魂掌", "掌", 96, "杨过独创，悲凉之极"),
    "弹指神通": Move("弹指神通", "指", 87, "东邪黄药师绝学"),
    "蛤蟆功": Move("蛤蟆功", "内功", 89, "西毒欧阳锋绝学"),
    "九阴真经": Move("九阴真经", "内功", 94, "武学至高秘籍"),
    "打狗棒法": Move("打狗棒法", "棍", 86, "丐帮帮主独门武学"),
    "七伤拳": Move("七伤拳", "拳", 91, "伤人亦伤己的霸道拳法"),
    "龙爪手": Move("龙爪手", "掌", 84, "刚猛凌厉的掌法")
}

# 招式相克关系：key克制value中的类型
COUNTER_SYSTEM = {
    "拳": ["掌", "棍"],
    "掌": ["指", "剑"],
    "指": ["拳", "内功"],
    "剑": ["拳", "棍"],
    "内功": ["掌", "剑"],
    "棍": ["指", "内功"]
}


# ==================== 角色系统 ====================

class Character:
    """角色类"""
    def __init__(self, name: str, title: str, base_power: int, specialty: str):
        self.name = name
        self.title = title
        self.base_power = base_power
        self.specialty = specialty
        self.coordination = 0  # 左右手协调度
        self.practice_count = 0  # 练习次数
        self.left_wins = 0  # 左手获胜次数
        self.right_wins = 0  # 右手获胜次数
        self.draws = 0  # 平局次数

    def get_proficiency(self) -> float:
        """计算熟练度"""
        return min(100, self.coordination / 10)

    def improve_coordination(self, amount: int):
        """提升协调度"""
        self.coordination += amount
        self.practice_count += 1


# 可选角色
CHARACTERS = {
    "1": Character("郭靖", "北侠", 90, "降龙十八掌"),
    "2": Character("小龙女", "古墓仙子", 88, "玉女心经"),
    "3": Character("杨过", "神雕侠", 92, "黯然销魂掌"),
    "4": Character("周伯通", "老顽童", 95, "左右互搏"),
}


# ==================== ASCII艺术 ====================

def show_ascii_art(art_type: str):
    """显示ASCII艺术"""
    arts = {
        "title": """
╔═══════════════════════════════════════╗
║     左  右  互  搏  术  练  习        ║
║                                       ║
║     Left-Right Fighting Training     ║
╚═══════════════════════════════════════╝
        """,
        "left_attack": """
        ╔══╗
    💪 ══╣👊╠═══>
        ╚══╝
        左手进攻！
        """,
        "right_attack": """
            ╔══╗
    <═══╣👊╠══ 💪
            ╚══╝
            右手进攻！
        """,
        "clash": """
        ╔══╗    ╔══╗
    💪═╣💥╠════╣💥╠═💪
        ╚══╝    ╚══╝
        激烈对抗！
        """,
        "victory": """
    　　　 ╔═══╗
    　　　 ║ 👑 ║
    　🎊 ╚═══╝ 🎊
    　   练习完成！
        """
    }
    print(arts.get(art_type, ""))


# ==================== 游戏逻辑 ====================

class ZuoYouHuBoGame:
    """左右互搏术游戏主类"""

    def __init__(self):
        self.character = None
        self.difficulty = "normal"
        self.round_count = 0

    def clear_screen(self):
        """清屏"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_menu(self):
        """显示主菜单"""
        self.clear_screen()
        show_ascii_art("title")
        print("\n欢迎来到左右互搏术练习系统！\n")
        print("请选择角色：")
        for key, char in CHARACTERS.items():
            print(f"{key}. {char.name}（{char.title}） - 擅长：{char.specialty}")
        print("\n0. 退出游戏")
        print("=" * 50)

    def select_character(self) -> bool:
        """选择角色"""
        choice = input("\n请输入角色编号：").strip()
        if choice == "0":
            return False
        if choice in CHARACTERS:
            self.character = CHARACTERS[choice]
            print(f"\n你选择了：{self.character.name}（{self.character.title}）")
            time.sleep(1)
            return True
        else:
            print("无效选择，请重新选择！")
            time.sleep(1)
            return self.select_character()

    def select_difficulty(self):
        """选择难度"""
        print("\n请选择练习难度：")
        print("1. 初学（Easy） - 10回合")
        print("2. 熟练（Normal） - 20回合")
        print("3. 精通（Hard） - 30回合")
        print("4. 宗师（Master） - 50回合")

        choice = input("\n请输入难度编号（默认2）：").strip() or "2"
        difficulty_map = {
            "1": ("easy", 10),
            "2": ("normal", 20),
            "3": ("hard", 30),
            "4": ("master", 50)
        }

        if choice in difficulty_map:
            self.difficulty, rounds = difficulty_map[choice]
            return rounds
        return 20

    def get_random_moves(self) -> Tuple[Move, Move]:
        """随机选择左右手招式"""
        move_list = list(MOVES.values())
        left_move = random.choice(move_list)
        right_move = random.choice(move_list)

        # 确保左右手招式不同
        while right_move.name == left_move.name:
            right_move = random.choice(move_list)

        return left_move, right_move

    def calculate_result(self, left_move: Move, right_move: Move) -> str:
        """计算对战结果"""
        # 基础威力
        left_power = left_move.power + random.randint(-10, 10)
        right_power = right_move.power + random.randint(-10, 10)

        # 添加角色加成
        left_power += self.character.base_power * 0.1
        right_power += self.character.base_power * 0.1

        # 相克判断
        left_counters_right = right_move.move_type in COUNTER_SYSTEM.get(left_move.move_type, [])
        right_counters_left = left_move.move_type in COUNTER_SYSTEM.get(right_move.move_type, [])

        if left_counters_right:
            left_power *= 1.3
        if right_counters_left:
            right_power *= 1.3

        # 判断胜负
        power_diff = abs(left_power - right_power)

        if power_diff < 15:
            self.character.draws += 1
            return "draw"
        elif left_power > right_power:
            self.character.left_wins += 1
            return "left"
        else:
            self.character.right_wins += 1
            return "right"

    def show_round_result(self, round_num: int, left_move: Move, right_move: Move, result: str):
        """显示回合结果"""
        print(f"\n{'='*60}")
        print(f"第 {round_num} 回合".center(56))
        print(f"{'='*60}")

        # 显示招式
        print(f"\n👈 左手：{left_move}")
        print(f"   {left_move.description}")
        print(f"\n👉 右手：{right_move}")
        print(f"   {right_move.description}")

        time.sleep(0.8)

        # 显示对战过程
        if result == "draw":
            show_ascii_art("clash")
            print("\n⚔️  势均力敌，难分高下！")
            coordination_gain = 5
        elif result == "left":
            show_ascii_art("left_attack")
            print("\n💪 左手占据上风！")
            coordination_gain = 3
        else:
            show_ascii_art("right_attack")
            print("\n💪 右手略胜一筹！")
            coordination_gain = 3

        # 检查相克
        left_counters = right_move.move_type in COUNTER_SYSTEM.get(left_move.move_type, [])
        right_counters = left_move.move_type in COUNTER_SYSTEM.get(right_move.move_type, [])

        if left_counters:
            print(f"✨ 左手{left_move.move_type}克制右手{right_move.move_type}！")
        if right_counters:
            print(f"✨ 右手{right_move.move_type}克制左手{left_move.move_type}！")

        # 更新协调度
        self.character.improve_coordination(coordination_gain)
        print(f"\n📈 左右手协调度提升 +{coordination_gain}")

    def show_progress_bar(self, current: int, total: int, bar_length: int = 30):
        """显示进度条"""
        progress = current / total
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = progress * 100
        print(f"\n进度: [{bar}] {percentage:.1f}% ({current}/{total})")

    def show_statistics(self, total_rounds: int):
        """显示统计信息"""
        print("\n" + "="*60)
        print("练习统计".center(56))
        print("="*60)

        print(f"\n角色：{self.character.name}（{self.character.title}）")
        print(f"总回合数：{total_rounds}")
        print(f"\n左手获胜：{self.character.left_wins} 次 ({self.character.left_wins/total_rounds*100:.1f}%)")
        print(f"右手获胜：{self.character.right_wins} 次 ({self.character.right_wins/total_rounds*100:.1f}%)")
        print(f"势均力敌：{self.character.draws} 次 ({self.character.draws/total_rounds*100:.1f}%)")

        proficiency = self.character.get_proficiency()
        print(f"\n当前熟练度：{proficiency:.1f}%")
        print(f"左右手协调度：{self.character.coordination}")

        # 评价
        if proficiency >= 90:
            evaluation = "🏆 宗师级！左右互搏已臻化境！"
        elif proficiency >= 70:
            evaluation = "⭐ 精通级！左右手已能完美配合！"
        elif proficiency >= 50:
            evaluation = "✨ 熟练级！左右手协调性大幅提升！"
        elif proficiency >= 30:
            evaluation = "💫 入门级！已初步掌握左右互搏要领！"
        else:
            evaluation = "🌱 初学者！继续努力练习吧！"

        print(f"\n{evaluation}")

        # 显示进步曲线
        print("\n熟练度进度：")
        self.show_progress_bar(int(proficiency), 100, 40)

    def start_practice(self):
        """开始练习"""
        rounds = self.select_difficulty()

        self.clear_screen()
        print(f"\n{self.character.name}开始左右互搏术练习！")
        print(f"难度：{self.difficulty.upper()}")
        print(f"回合数：{rounds}")
        print("\n按回车键继续...")
        input()

        # 练习循环
        for round_num in range(1, rounds + 1):
            self.clear_screen()

            # 获取随机招式
            left_move, right_move = self.get_random_moves()

            # 计算结果
            result = self.calculate_result(left_move, right_move)

            # 显示结果
            self.show_round_result(round_num, left_move, right_move, result)

            # 显示当前进度
            self.show_progress_bar(round_num, rounds)

            if round_num < rounds:
                print("\n按回车继续下一回合...")
                input()
            else:
                time.sleep(1)

        # 显示最终统计
        self.clear_screen()
        show_ascii_art("victory")
        self.show_statistics(rounds)

    def run(self):
        """运行游戏主循环"""
        while True:
            self.show_menu()

            if not self.select_character():
                print("\n感谢游玩！江湖再见！👋")
                break

            self.start_practice()

            print("\n" + "="*60)
            choice = input("\n是否继续练习？(y/n)：").strip().lower()
            if choice != 'y':
                print("\n感谢游玩！江湖再见！👋")
                break


# ==================== 主程序入口 ====================

def main():
    """主函数"""
    try:
        game = ZuoYouHuBoGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n程序已退出。江湖再见！👋")
    except Exception as e:
        print(f"\n程序出错：{e}")


if __name__ == "__main__":
    main()

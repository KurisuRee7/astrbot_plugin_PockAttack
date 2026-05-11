import random
import time
import re
from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import astrbot.api.message_components as Comp

# 关键词列表
keywords = ["攻击", "猛攻", "戳", "草饲", "曹飞"]
# 冷却话术列表
cooling_down_messages = [
    "人家戳到手疼了，晚点再玩嘛。",
    "让我歇会儿，等下再戳。",
    "我累啦，过会儿再继续。"
]
# 不能自己戳自己的话术列表
self_poke_messages = [
    "让你戳了吗",
    "别让我自己戳自己啦，很奇怪的。",
    "我才不要自己戳自己呢。",
    "贼子尔敢！"
]
# 收到指令的回复话术列表
received_commands_messages = [
    "虎！虎！虎！",
    "草饲！",
    "爆炒！",
    "收到收到！",
    "猛攻！"
]

powering_txt = [
    "超级必杀技！",
    "点火！",
    "灼日凌空！",
    "此刻，见证终焉之光！",
    "Excalibur！！",
    "惩罚，在此降临！",
    "翱翔天际！",
    "Sei, Sei! koi gigi!",
    "时间差不多咯",
    "It's high noon...",
    "感受 我的痛苦！",
    "葬灭！"
]

ultra_poke = [
    "爆裂推进！",
    "越过迷雾！与深渊！！",
    "为了十字军！",
    "毁天灭地！",
    "清算时间到！",
    "拔枪！",
    "Pi！Ka！Chu！！",
    "死告天使！",
    "就由我来演奏终曲！",
    "崩裂的束缚，化为利刃！",
    "狂澜，分割天地！",
    "此剑，斩灭诸恶！",
    "一瞬千击！",
    "燃魂淬骨！",
    "聆听 死亡的终音!"
]

end_txt = [
    "搞定！😘",
    "收工！🥰",
    "赫赫，不会坏掉了吧🤭",
    "累 累死了😪",
    "燃尽了😴"
]

group_list = [
    #  "758575911"
     
]

@register("PockAttack", "Louie", "戳一戳攻击插件", "1.0.0", "https://github.com/yourrepo")
class PokeAttack(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.cooling_down = False
        self.cooling_end_time = 0

    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def handle_group_message(self, event: AstrMessageEvent):
        message_obj = event.message_obj # 获取消息对象
        message_str = message_obj.message_str # 消息文本内容
        self_id = event.get_self_id() # 机器人QQ号
        group_id = message_obj.group_id # 群号

        # 检查消息开头是否有关键词
        for keyword in keywords:
            if message_str.startswith(keyword):
                if random.random() < 0.3 and event.get_group_id() not in group_list:
                    # if re.match(rf'^{keyword}(！|!)$', message_str):
                    # 再随机决定是否触发强化版戳一戳
                    # rand_val = random.random()
                    # print(f"Random value: {rand_val}")
                
                    # 确定戳一戳的次数 (有感叹号会触发更多戳戳)
                    powering_time = random.uniform(1.2, 2)
                    poke_times = round(powering_time * 5)

                    # 提取消息中 @ 的用户
                    messages = event.get_messages()
                    target_user_id = next((str(seg.qq) for seg in messages if (isinstance(seg, Comp.At))), None)

                    # 检查是否有 @ 的用户
                    if target_user_id is None:
                        return
                    # 检查受击人是否机器人本体
                    if str(target_user_id) == str(self_id):
                        yield event.plain_result(random.choice(self_poke_messages)) # self_poke_messages 为不能自己戳自己的话术列表
                        return
                    
                    # 检查是否在冷却期
                    if self.cooling_down and time.time() < self.cooling_end_time:
                        yield event.plain_result(random.choice(cooling_down_messages))
                        return
                    
                    # 攻击前自嗨
                    yield event.plain_result(random.choice(powering_txt))
                    time.sleep(powering_time)
                    yield event.plain_result(random.choice(ultra_poke))
                    
                    # 发送戳一戳
                    payloads = {"user_id": target_user_id, "group_id": group_id}
                    for _ in range(poke_times):
                        try:
                            await event.bot.api.call_action('send_poke', **payloads)
                        except Exception as e:
                            yield event.plain_result("插件出错，请联系管理员关闭插件")
                            pass
                    time.sleep(1)
                    yield event.plain_result(random.choice(end_txt))

                    # 进入冷却期
                    self.cooling_down = True
                    cooling_duration = random.randint(5, 10)
                    self.cooling_end_time = time.time() + cooling_duration
                    return
                else:
                    # 确定戳一戳的次数 (有感叹号会触发更多戳戳)
                    if re.match(rf'^{keyword}(！|!)$', message_str):
                            poke_times = random.randint(3, 5)
                    else:
                        poke_times = random.randint(2, 4)

                    # 提取消息中 @ 的用户
                    messages = event.get_messages()
                    target_user_id = next((str(seg.qq) for seg in messages if (isinstance(seg, Comp.At))), None)

                    # 检查是否有 @ 的用户
                    if target_user_id is None:
                        return
                    # 检查受击人是否机器人本体
                    if str(target_user_id) == str(self_id):
                        yield event.plain_result(random.choice(self_poke_messages)) # self_poke_messages 为不能自己戳自己的话术列表
                        return
                    
                    # 检查是否在冷却期
                    if self.cooling_down and time.time() < self.cooling_end_time:
                        yield event.plain_result(random.choice(cooling_down_messages))
                        return
                    
                    # 攻击前自嗨
                    yield event.plain_result(random.choice(received_commands_messages))

                    # 发送戳一戳
                    payloads = {"user_id": target_user_id, "group_id": group_id}
                    for _ in range(poke_times):
                        try:
                            await event.bot.api.call_action('send_poke', **payloads)
                        except Exception as e:
                            yield event.plain_result("插件出错，请联系管理员关闭插件")
                            pass

                    # 进入冷却期
                    self.cooling_down = True
                    cooling_duration = random.randint(5, 10)
                    self.cooling_end_time = time.time() + cooling_duration
                    return

    

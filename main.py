import random
import time
from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import astrbot.api.message_components as Comp
import asyncio
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

@register("PockAttack", "KurisuRee7", "戳一戳攻击插件", "1.0.0", "https://github.com/KurisuRee7/astrbot_plugin_PockAttack")
class PokeAttack(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.group_cooling = {}

    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def handle_group_message(self, event: AstrMessageEvent):
        message_obj = event.message_obj
        message_str = message_obj.message_str
        self_id = event.get_self_id()
        group_id = message_obj.group_id
    
        for keyword in keywords:
            if message_str.startswith(keyword):
                # 判断是否有感叹号
                has_exclamation = (
                        message_str.startswith(keyword + "！")
                        or
                        message_str.startswith(keyword + "!")
                    )
                
                # 提取 @ 的用户
                messages = event.get_messages()
                target_user_id = next((str(seg.qq) for seg in messages if isinstance(seg, Comp.At)), None)
                
                if target_user_id is None:
                    return
                
                if str(target_user_id) == str(self_id):
                    yield event.plain_result(random.choice(self_poke_messages))
                    return
                
                cooling_end_time = self.group_cooling.get(group_id, 0)
                if time.time() < cooling_end_time:
                    yield event.plain_result(random.choice(cooling_down_messages))
                    return
                
                # 30% 概率触发 powering 分支
                if random.random() < 0.3:
                    if has_exclamation:
                        powering_time = random.uniform(1.5, 2.5)  # 有感叹号，更长
                    else:
                        powering_time = random.uniform(1.0, 1.8)  # 无感叹号，较短
                    
                    poke_times = round(powering_time * 5)  # 5-12次 vs 5-9次
                    
                    yield event.plain_result(random.choice(powering_txt))
                    await asyncio.sleep(powering_time)
                    yield event.plain_result(random.choice(ultra_poke))
                    
                    payloads = {"user_id": target_user_id, "group_id": group_id}
                    for _ in range(poke_times):
                        try:
                            await event.bot.api.call_action('send_poke', **payloads)
                        except Exception:
                            yield event.plain_result("插件出错，请联系管理员关闭插件")
                            pass
                    
                    await asyncio.sleep(1)
                    yield event.plain_result(random.choice(end_txt))
                    
                else:
                    # ========== 普通分支 ==========
                    if has_exclamation:
                        poke_times = random.randint(3, 5)   # 有感叹号，3-5次
                    else:
                        poke_times = random.randint(2, 4)   # 无感叹号，2-4次
                    
                    yield event.plain_result(random.choice(received_commands_messages))
                    
                    payloads = {"user_id": target_user_id, "group_id": group_id}
                    for _ in range(poke_times):
                        try:
                            await event.bot.api.call_action('send_poke', **payloads)
                        except Exception:
                            yield event.plain_result("插件出错，请联系管理员关闭插件")
                            pass
                
                # 进入冷却期（两个分支共用）
                cooling_duration = random.randint(5, 10)
                self.group_cooling[group_id] = time.time() + cooling_duration
                return
        

# GoIP SIM ревизия + тарифы PAYG + MCP — снапшот 26.08.2026

## Что сделано
- **Тарифы PAYG (главная задача) — выполнено.** Все рабочие карты на pay-as-you-go без ежедневных списаний, интернет не расходуется.
  - Lyca x4 (GoIP-8 L1/L2, GoIP-4 L1/L4) — уже на PAYG, пакеты истекли (*137# = pacote expirou).
  - MEO L7 (+351927596298) — переведён на M Movel Livre (0.06E/мин, без абонплаты) через my.meo.pt: Servicos -> Tarifario -> Alterar -> M Movel Livre. Без SMS-кода.
  - Vodafone L4 (+351913651286), NOS L5 (+351937656543) — чистые prepaid без пакетов.
  - MEO L8 (-2.50E) — оставлена как есть (номер неизвестен, ЛК недоступен, минус нейтрализует пакет).
- **MCP-сервер ChatGPT** закреплён под systemd (goip-private-mcp.service, active+enabled, 11 инструментов, порт 18765, URL goip.smartcare.house/{TOKEN}/mcp). Был nohup + бесконечный рестарт из-за занятого порта — устранено.
- **Активация карт:** GoIP-8 L4 Vodafone + L5 NOS подняты (PIN через Configurations->SIM + ручное включение модуля status.html?type=list&down=0&line=N).
- **Инструкция активации SIM** для новых пользователей создана в Notion.

## Решения
- MEO L8 не реанимировать сейчас (номер неизвестен).
- Смена тарифа MEO только через my.meo.pt (USSD *123# не работает).
- ОПАСНО: раздел "Ativar cartao / 2a via" в ЛК MEO убивает карту в гейте — не нажимать.
- Раздельные SIP-логины для определения номеров НЕ работают (метка даёт привязку только для известного номера).
- MB WAY работает для пополнения (L7 пополнена).

## Открытия
- GoIP-8 L3 = Lyca ITALY (не Portugal).
- USSD-меню NOS поддерживает продолжение сессии цифрой (MEO не поддерживает).
- Коды Vodafone: баланс *#123#, свой номер *#122#.

## Осталось (PENDING)
- Активация WOO (GoIP-4 L2) и WTF (GoIP-4 L3) через приложение оператора — нужны стартовые пакеты карт.
- Пополнить L4 Vodafone (откроет исходящие -> номер) и L8 MEO.
- Номера приём-онли L3/L6/L8 определятся когда карты смогут исходящие.

## Карта парка
GoIP-8: L1 Lyca +351920714158 5.15E | L2 Lyca +351920711655 3.70E | L3 Lyca-IT recv-only | L4 Vodafone +351913651286 2.50E recv-ok | L5 NOS +351937656543 2.15E | L6 recv-only | L7 MEO +351927596298 2.50E PAYG | L8 MEO -2.50E num?
GoIP-4: L1 Lyca +351920147613 0.53E | L2 WOO offline(activation) | L3 WTF offline(activation) | L4 Lyca +351920479292 5.00E

## Ссылки
- dispatcher-core: project goippro (id 5), task GOIP-SIM-TARIFFS-001, handoff hoff-c1ad50ec5830, snapshot snap-b902566c5e0c
- ai-memory: notes/goip-sim-tariffs-mcp-snapshot-20260826.md
- Notion парк: 34350f3b-8104-81fd-b7ac-e89c8219f64e ; инструкция активации: 3c850f3b-8104-81af-b960-e8262af298f3
- PostgreSQL: goip_progress_log id 1

_DISCLMAIMER: Esse texto foi gerado por IA_
# 🍅 Pomodoro Timer

Um timer Pomodoro no terminal construído com Textual TUI — meu primeiro projeto explorando o Textual e o uv como gerenciador de pacotes moderno.

https://github.com/user-attachments/assets/0cc4bb6a-2142-443f-acf0-3ba6e4fca112

## Funcionalidades

- Fases automáticas: Foco (25min) → Pausa (5min) → Pausa Longa (15min) a cada 3 ciclos
- Transição automática entre fases com sinal visual
- Botões de Start, Pause, Stop e Skip
- Configuração via arquivo `pomodoro.toml`

## Configuração

As durações e número de ciclos podem ser alterados no `pomodoro.toml`:

```toml
[phases]
focus_duration = 1500           # 25 min em segundos
break_duration = 300            # 5 min
long_break_duration = 900       # 15 min
cycles_before_long_break = 3
```

## Como rodar

Instale o [uv](https://docs.astral.sh/uv/) e rode:

```bash
uv sync
uv run pomodoro
```

## Tecnologias

- [Textual](https://github.com/Textualize/textual) — framework para TUIs em Python
- [uv](https://docs.astral.sh/uv/) — gerenciador de pacotes e projetos Python


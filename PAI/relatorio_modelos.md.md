# Relatório de Experimentação e Avaliação de Modelos de Linguagem — Sprint 03

## 1. Modelos Avaliados e Configurações

O núcleo conversacional da solução EV ChargeOps GoodWe foi submetido a uma bateria de testes executando o OpenAI Agents SDK com dois modelos de linguagem distintos e configurações de hiperparâmetros padronizadas.

| Parâmetro | Configuração A (Padrão) | Configuração B (Criativa) |
| :--- | :--- | :--- |
| **Modelos Testados** | `gpt-4o-mini`, `gpt-4o` | `gpt-4o-mini`, `gpt-4o` |
| **Temperature** | `0.2` | `0.7` |
| **Top_P** | `0.9` | `0.95` |
| **Max Tokens** | `500` | `800` |

---

## 2. Resultados dos Testes

Foram executados 20 casos de teste (10 funcionais, 5 de memória de curto/longo prazo e 5 de segurança e guardrails).

| Modelo / Configuração | Taxa de Sucesso Funcional | Aderência à Memória | Resistência a Injection | Latência Média | Custo Est. / 1k Tokens |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT-4o-mini (Temp 0.2)** | 95% | 100% | 100% (via SDK) | 0.85s | $0.00015 |
| **GPT-4o-mini (Temp 0.7)** | 85% | 90% | 100% (via SDK) | 0.88s | $0.00015 |
| **GPT-4o (Temp 0.2)** | 100% | 100% | 100% (via SDK) | 1.42s | $0.00250 |
| **GPT-4o (Temp 0.7)** | 90% | 95% | 100% (via SDK) | 1.50s | $0.00250 |

---

## 3. Análise Qualitativa e Diferenças Percebidas

1. **`gpt-4o-mini` (Temperatura Baixa - 0.2):**
   * **Vantagens:** Extremamente rápido, custo quase irrelevante, alta fidelidade às instruções do `SYSTEM_PROMPT` e excelente recuperação de contexto quando acoplado ao `SQLiteSession`.
   * **Limitações:** Respostas ligeiramente mais mecânicas e diretas.

2. **`gpt-4o` (Temperatura 0.2 / 0.7):**
   * **Vantagens:** Superior na articulação de explicações técnicas sobre rateio de tarifas ANEEL e protocolo OCPP.
   * **Limitações:** Latência 67% maior e custo significativamente superior sem um ganho proporcional em tarefas conversacionais de nível N1/N2 de atendimento.

3. **Efeito da Temperatura:**
   * Temperaturas mais altas (`0.7`) causaram respostas mais prolixas e, em 2 casos, o agente tendeu a inventar prazos genéricos de manutenção que não estavam especificados na base da GoodWe.

---

## 4. Modelo Escolhido e Justificativa

* **Modelo Final Escolhido:** `gpt-4o-mini`
* **Configuração:** `temperature=0.2`, `top_p=0.9`, `max_tokens=500`.
* **Justificativa:** O `gpt-4o-mini` operando dentro da arquitetura OpenAI Agents SDK atendeu 100% dos requisitos de memória e de segurança (devido aos Input Guardrails rodando nativamente em código). Ele oferece uma latência média abaixo de 1 segundo e um custo-benefício ideal para operações de atendimento em tempo real de condomínios.
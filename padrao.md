# Padronizacao
Preferi padronizar as variáveis para que não houvesse dúvidas sobre o que chamar, e também para não ficar confuso quando for ler diferentes funções que utilizam as mesmas variáveis.
### Para variaveis dos arquivos familia:
- familia:dict[str, dict[str, list[str] | str | float]] - referente as linguas que compõe o ramo/família. Exemplo: fm.dialetos_criados
- dicionario:dict[str, list[str] | str | float] - referente a todas as palavras contidas em uma língua. Exemplo: fm.dialetos_criados[lingua_a]["lingua"], isso mostra todas as palavras existentes nessa língua, como se fosse um livro de palavras.
- configuracao:dict[str, float] - referente às probabilidades de mudanças/conservações de cada língua. Exemplo: fm.dialetos_criados[lingua_a]["configuracao"]

### Para colang.ipynb:
- Aqui é possível usar à sua vontade. Como é um arquivo dedicado para visualização dos comandos, não tem impacto real a mudança de variável.

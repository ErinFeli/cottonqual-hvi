# CottonQual

Aplicacao Streamlit para diagnostico de qualidade HVI, importacao de laudos, simulacao de blending e estimativa de preco do algodao.

## Executar localmente

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Acessibilidade e tema

A interface oferece navegação por teclado com foco visível, textos com contraste reforçado, rótulos descritivos para os campos e alternativas textuais para os gráficos. Use o botão na barra lateral para alternar entre os temas claro e escuro; a escolha vale durante a sessão atual.

## Publicar gratuitamente

O caminho mais direto e o [Streamlit Community Cloud](https://streamlit.io/cloud). Para este fluxo gratuito, o codigo precisa estar em um repositorio GitHub publico, e o app publicado tambem ficara acessivel publicamente.

1. Envie `app.py`, `requirements.txt` e `.streamlit/config.toml` para um repositorio GitHub publico.
2. Entre no Community Cloud usando o GitHub e escolha **Create app**.
3. Selecione o repositorio, a branch e `app.py` como arquivo principal; depois escolha **Deploy**.

Nao envie credenciais nem `.streamlit/secrets.toml` ao repositorio.
import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🤖 Práctica: Creación de un Chatbot con Interfaz Visual\n",
    "## Módulo: Modelos de Inteligencia Artificial (5071)\n",
    "\n",
    "En esta práctica vamos a desplegar un modelo de lenguaje generativo utilizando la arquitectura **Transformer** y crearemos una interfaz web interactiva con **Gradio**."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. Instalación de dependencias\n",
    "Instalamos `transformers` para los modelos, `torch` para el motor de tensores y `gradio` para la interfaz."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install transformers torch gradio"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. Configuración del Modelo y Lógica de Chat\n",
    "Utilizaremos **Blenderbot** de Facebook, un modelo optimizado para mantener conversaciones coherentes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import gradio as gr\n",
    "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer\n",
    "import torch\n",
    "\n",
    "# Carga del modelo y tokenizador\n",
    "model_name = \"facebook/blenderbot-400M-distill\"\n",
    "tokenizer = AutoTokenizer.from_pretrained(model_name)\n",
    "model = AutoModelForSeq2SeqLM.from_pretrained(model_name)\n",
    "\n",
    "def predict(message, history):\n",
    "    # Construcción del contexto del historial\n",
    "    history_transformer_format = \"\"\n",
    "    for human, assistant in history:\n",
    "        history_transformer_format += human + \" </s> \" + assistant + \" </s> \"\n",
    "    history_transformer_format += message + \" </s> \"\n",
    "\n",
    "    # Tokenización y generación\n",
    "    inputs = tokenizer(history_transformer_format, return_tensors=\"pt\")\n",
    "    \n",
    "    with torch.no_grad():\n",
    "        output_tokens = model.generate(\n",
    "            **inputs, \n",
    "            max_length=100, \n",
    "            do_sample=True, \n",
    "            top_p=0.9, \n",
    "            temperature=0.7 # Ajusta la 'creatividad'\n",
    "        )\n",
    "\n",
    "    response = tokenizer.decode(output_tokens[0], skip_special_tokens=True)\n",
    "    return response"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3. Lanzamiento de la Interfaz\n",
    "Ejecuta esta celda para generar una URL pública y probar tu Chatbot."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "demo = gr.ChatInterface(\n",
    "    fn=predict,\n",
    "    title=\"🤖 Mi Primer Chatbot - Especialización IA\",\n",
    "    description=\"Interactúa con un modelo Transformer. Prueba a cambiar la temperatura en el código para ver cómo varían las respuestas.\",\n",
    "    theme=\"soft\"\n",
    ")\n",
    "\n",
    "demo.launch(share=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open("Practica_Chatbot_IA.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print("✅ Notebook 'Practica_Chatbot_IA.ipynb' generado con éxito.")
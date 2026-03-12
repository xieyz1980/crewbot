#!/usr/bin/env python3
"""
Docker AI模型推理服务
支持GPU加速，使用HuggingFace Transformers
"""

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 全局变量存储模型和tokenizer
model = None
tokenizer = None

def load_model():
    """加载模型到GPU"""
    global model, tokenizer
    
    model_name = os.getenv('MODEL_NAME', 'TinyLlama/TinyLlama-1.1B-Chat-v1.0')
    hf_token = os.getenv('HF_TOKEN')
    
    logger.info(f"正在加载模型: {model_name}")
    logger.info(f"CUDA可用: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    
    # 配置4bit量化
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=hf_token,
        trust_remote_code=True
    )
    
    # 设置padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # 加载模型到GPU
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map='auto',
        torch_dtype=torch.float16,
        token=hf_token,
        trust_remote_code=True
    )
    
    logger.info("模型加载完成！")
    logger.info(f"模型内存占用: {model.get_memory_footprint() / 1e9:.2f} GB")

def format_prompt(prompt, model_name):
    """根据模型类型格式化prompt"""
    if 'llama' in model_name.lower() or 'tinyllama' in model_name.lower():
        return f"<|user|>\n{prompt}</s>\n<|assistant|>\n"
    elif 'qwen' in model_name.lower():
        return f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    elif 'mistral' in model_name.lower():
        return f"[INST] {prompt} [/INST]"
    else:
        return prompt

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'service': 'Docker AI Model Inference API',
        'model': os.getenv('MODEL_NAME', 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'),
        'endpoints': {
            '/health': '健康检查',
            '/generate': '文本生成 (POST)',
            '/info': '模型信息'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'gpu_available': torch.cuda.is_available(),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        'cuda_version': torch.version.cuda if torch.cuda.is_available() else None
    })

@app.route('/info', methods=['GET'])
def info():
    """模型信息接口"""
    model_name = os.getenv('MODEL_NAME', 'TinyLlama/TinyLlama-1.1B-Chat-v1.0')
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9 if torch.cuda.is_available() else 0
    
    return jsonify({
        'model_name': model_name,
        'gpu_available': torch.cuda.is_available(),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        'gpu_memory_gb': round(gpu_memory, 2),
        'model_loaded': model is not None
    })

@app.route('/generate', methods=['POST'])
def generate():
    """文本生成接口"""
    try:
        data = request.json or {}
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'prompt不能为空'}), 400
        
        max_length = data.get('max_length', 512)
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 0.9)
        
        model_name = os.getenv('MODEL_NAME', 'TinyLlama/TinyLlama-1.1B-Chat-v1.0')
        formatted_prompt = format_prompt(prompt, model_name)
        
        logger.info(f"生成请求: {prompt[:50]}...")
        
        # 编码输入
        inputs = tokenizer(
            formatted_prompt,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=2048
        ).to('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 生成文本
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
                num_return_sequences=1
            )
        
        # 解码输出（只取生成的新内容）
        generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
        generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        logger.info(f"生成完成，长度: {len(generated_text)} 字符")
        
        return jsonify({
            'prompt': prompt,
            'generated': generated_text.strip(),
            'model': model_name,
            'parameters': {
                'max_length': max_length,
                'temperature': temperature,
                'top_p': top_p
            }
        })
    
    except Exception as e:
        logger.error(f"生成错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_batch', methods=['POST'])
def generate_batch():
    """批量文本生成接口"""
    try:
        data = request.json or {}
        prompts = data.get('prompts', [])
        
        if not prompts or not isinstance(prompts, list):
            return jsonify({'error': 'prompts必须是字符串数组'}), 400
        
        max_length = data.get('max_length', 512)
        temperature = data.get('temperature', 0.7)
        
        model_name = os.getenv('MODEL_NAME', 'TinyLlama/TinyLlama-1.1B-Chat-v1.0')
        formatted_prompts = [format_prompt(p, model_name) for p in prompts]
        
        logger.info(f"批量生成请求: {len(prompts)} 条")
        
        # 批量编码
        inputs = tokenizer(
            formatted_prompts,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=2048
        ).to('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 批量生成
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        # 解码所有输出
        results = []
        for i, output in enumerate(outputs):
            input_len = inputs['input_ids'][i].shape[0]
            generated_tokens = output[input_len:]
            generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            results.append({
                'prompt': prompts[i],
                'generated': generated_text.strip()
            })
        
        logger.info(f"批量生成完成")
        
        return jsonify({
            'results': results,
            'model': model_name,
            'count': len(results)
        })
    
    except Exception as e:
        logger.error(f"批量生成错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 启动时加载模型
    load_model()
    
    # 启动Flask服务
    logger.info("启动API服务，端口: 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

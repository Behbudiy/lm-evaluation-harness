# FLORES+ Uzbek-English-Russian Translation

## Overview

This benchmark evaluates machine translation performance between Uzbek, English, and Russian using the FLORES+ dataset.

## Dataset

- **Source**: [openlanguagedata/flores_plus](https://huggingface.co/datasets/openlanguagedata/flores_plus)
- **Languages**:
  - Uzbek (Northern Uzbek, Latin script: `uzn_Latn`)
  - English (Latin script: `eng_Latn`)
  - Russian (Cyrillic script: `rus_Cyrl`)
- **Splits**:
  - `dev`: 997 examples (used for few-shot)
  - `devtest`: 1,012 examples (used for evaluation)

## Tasks

### 1. `flores_plus_uz_en` - Uzbek to English
Translates Uzbek sentences to English.

**Prompt format**:
```
Uzbek sentence: [Uzbek text]

English sentence:
```

### 2. `flores_plus_en_uz` - English to Uzbek
Translates English sentences to Uzbek.

**Prompt format**:
```
English sentence: [English text]

Uzbek sentence:
```

### 3. `flores_plus_uz_ru` - Uzbek to Russian
Translates Uzbek sentences to Russian.

**Prompt format**:
```
Uzbek sentence: [Uzbek text]

Russian sentence:
```

### 4. `flores_plus_ru_uz` - Russian to Uzbek
Translates Russian sentences to Uzbek.

**Prompt format**:
```
Russian sentence: [Russian text]

Uzbek sentence:
```

## Metrics

- **BLEU**: Bilingual Evaluation Understudy (higher is better)
- **chrF**: Character n-gram F-score (higher is better)
- **TER**: Translation Error Rate (lower is better)

## Usage

### Evaluate all directions (Uz↔En↔Ru):
```bash
lm_eval --model hf \
  --model_args pretrained=your-model-name \
  --tasks flores_plus \
  --num_fewshot 5 \
  --device cuda \
  --batch_size auto
```

### Evaluate specific language pairs:

**Uzbek↔English:**
```bash
lm_eval --model hf \
  --model_args pretrained=your-model-name \
  --tasks flores_plus_uz_en,flores_plus_en_uz \
  --num_fewshot 5 \
  --device cuda
```

**Uzbek↔Russian:**
```bash
lm_eval --model hf \
  --model_args pretrained=your-model-name \
  --tasks flores_plus_uz_ru,flores_plus_ru_uz \
  --num_fewshot 5 \
  --device cuda
```

### Evaluate single direction:
```bash
# Uzbek → English
lm_eval --model hf --model_args pretrained=your-model --tasks flores_plus_uz_en --num_fewshot 5

# English → Uzbek
lm_eval --model hf --model_args pretrained=your-model --tasks flores_plus_en_uz --num_fewshot 5

# Uzbek → Russian
lm_eval --model hf --model_args pretrained=your-model --tasks flores_plus_uz_ru --num_fewshot 5

# Russian → Uzbek
lm_eval --model hf --model_args pretrained=your-model --tasks flores_plus_ru_uz --num_fewshot 5
```

## Few-Shot Recommendations

- **0-shot**: Tests model's inherent translation ability
- **1-shot**: Minimal demonstration
- **5-shot**: Standard for translation benchmarks (recommended)

## Generation Parameters

The benchmark uses greedy decoding by default:
- `temperature: 0.0` - Greedy decoding for reproducibility
- `do_sample: false` - Deterministic generation
- `max_gen_toks: 256` - Maximum tokens to generate
- `until: ["\n", ...]` - Stops at newline OR any EOS token (whichever comes first)

### Supported EOS Tokens

The benchmark stops at the first occurrence of:
- `\n` - Primary stopping criterion (single sentence)
- `</s>` - Mistral, LLaMA 2, older models
- `<eos>` - Gemma 2/3 base models
- `<|end_of_text|>` - LLaMA 3 base models
- `<|eot_id|>` - LLaMA 3 instruct models
- `<|endoftext|>` - GPT-2, Phi, Qwen 2.5 base
- `<|im_end|>` - Qwen 2.5 instruct (ChatML format)
- `<end_of_turn>` - Gemma 2/3 instruct models

**Why multiple EOS tokens?**
- Ensures fair cross-model comparison
- Works with both base and instruct-tuned models
- Respects each model's natural stopping behavior
- Standard practice for multi-model benchmarking

**Model-Specific Behavior:**
| Model Family | Base EOS | Instruct EOS |
|--------------|----------|--------------|
| Gemma 2/3 | `<eos>` | `<end_of_turn>` |
| LLaMA 3 | `<|end_of_text|>` | `<|eot_id|>` |
| Qwen 2.5 | `<|endoftext|>` | `<|im_end|>` |
| Mistral | `</s>` | `</s>` |
| Phi | `<|endoftext|>` | `<|endoftext|>` |

For different generation strategies, modify `_flores_plus_common_yaml`.

## Citation

If you use this benchmark, please cite the FLORES+ dataset:

```bibtex
@inproceedings{nllb2022,
  title={No Language Left Behind: Scaling Human-Centered Machine Translation},
  author={{NLLB Team} and Costa-jussà, Marta R. and Cross, James and Çelebi, Onur and others},
  year={2022}
}
```

## Version

- **Version**: 1.0
- **Date**: 2025-01-18

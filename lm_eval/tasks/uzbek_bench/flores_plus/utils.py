"""Utility functions for FLORES+ Uzbek-English-Russian translation tasks."""

from datasets import load_dataset, Dataset


def flores_plus_doc_to_text_uz_en(doc):
    """Convert Uzbek→English translation doc to prompt text."""
    return f"Uzbek sentence: {doc['text_uzn_Latn']}\n\nEnglish sentence:"


def flores_plus_doc_to_text_en_uz(doc):
    """Convert English→Uzbek translation doc to prompt text."""
    return f"English sentence: {doc['text_eng_Latn']}\n\nUzbek sentence:"


def flores_plus_doc_to_target_uz_en(doc):
    """Extract English target for Uzbek→English translation."""
    return doc['text_eng_Latn']


def flores_plus_doc_to_target_en_uz(doc):
    """Extract Uzbek target for English→Uzbek translation."""
    return doc['text_uzn_Latn']


def flores_plus_doc_to_text_uz_ru(doc):
    """Convert Uzbek→Russian translation doc to prompt text."""
    return f"Uzbek sentence: {doc['text_uzn_Latn']}\n\nRussian sentence:"


def flores_plus_doc_to_text_ru_uz(doc):
    """Convert Russian→Uzbek translation doc to prompt text."""
    return f"Russian sentence: {doc['text_rus_Cyrl']}\n\nUzbek sentence:"


def flores_plus_doc_to_target_uz_ru(doc):
    """Extract Russian target for Uzbek→Russian translation."""
    return doc['text_rus_Cyrl']


def flores_plus_doc_to_target_ru_uz(doc):
    """Extract Uzbek target for Russian→Uzbek translation."""
    return doc['text_uzn_Latn']


def flores_plus_process_docs(dataset):
    """
    Merge Uzbek, English, and Russian FLORES+ datasets.

    FLORES+ stores each language in a separate config, so we need to
    load all languages and merge them by ID.

    This function receives a Dataset object for a single split and returns
    a merged Dataset with Uzbek, English, and Russian texts.
    """
    # The dataset parameter is the Uzbek dataset loaded by lm-eval
    # We need to load the corresponding English and Russian datasets

    # Determine which split this is based on the dataset size
    # dev: 997 examples, devtest: 1012 examples
    split_name = 'dev' if len(dataset) == 997 else 'devtest'

    # Load English and Russian datasets for the same split
    ds_en = load_dataset(
        'openlanguagedata/flores_plus',
        'eng_Latn',
        split=split_name
    )
    ds_ru = load_dataset(
        'openlanguagedata/flores_plus',
        'rus_Cyrl',
        split=split_name
    )

    # Merge by creating new examples with all three language texts
    merged = []
    for uz_example, en_example, ru_example in zip(dataset, ds_en, ds_ru):
        # Verify IDs match
        assert uz_example['id'] == en_example['id'] == ru_example['id'], \
            f"ID mismatch: {uz_example['id']}, {en_example['id']}, {ru_example['id']}"

        merged.append({
            'id': uz_example['id'],
            'text_uzn_Latn': uz_example['text'],
            'text_eng_Latn': en_example['text'],
            'text_rus_Cyrl': ru_example['text'],
            'url': uz_example.get('url', ''),
            'domain': uz_example.get('domain', ''),
            'topic': uz_example.get('topic', ''),
        })

    return Dataset.from_list(merged)

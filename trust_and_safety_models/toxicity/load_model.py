import os

import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification

from toxicity_ml_pipeline.utils.helpers import execute_command

LOCAL_MODEL_DIR = os.path.join('toxicity_ml_pipeline', 'models')
LOCAL_DIR = os.path.join('toxicity_ml_pipeline', 'data')
MAX_SEQ_LENGTH = 512


def reload_model_weights(weights_dir, language, **kwargs):
    optimizer = tf.keras.optimizers.Adam(0.01)
    model_type = (
        "twitter_bert_base_en_uncased_mlm"
        if language == "en"
        else "twitter_multilingual_bert_base_cased_mlm"
    )
    model = load(optimizer=optimizer, seed=42, model_type=model_type, **kwargs)
    model.load_weights(weights_dir)
    return model


def _locally_copy_models(model_type):
    if model_type == "twitter_multilingual_bert_base_cased_mlm":
        preprocessor = "bert_multi_cased_preprocess_3"
    elif model_type == "twitter_bert_base_en_uncased_mlm":
        preprocessor = "bert_en_uncased_preprocess_3"
    else:
        raise NotImplementedError
    local_preprocessor_path = os.path.join(LOCAL_MODEL_DIR, preprocessor)
    if not os.path.exists(local_preprocessor_path):
        copy_cmd = f"mkdir -p {LOCAL_MODEL_DIR}; gsutil -m cp -r gs://... {LOCAL_MODEL_DIR}"
        execute_command(copy_cmd.format(model_type=model_type, preprocessor=preprocessor))
    return preprocessor


def load_encoder(model_type, trainable):
    try:
        model = TextEncoder(
            max_seq_lengths=MAX_SEQ_LENGTH,
            model_type=model_type,
            cluster="gcp",
            trainable=trainable,
            enable_dynamic_shapes=True,
        )
    except (OSError, tf.errors.AbortedError):
        preprocessor = _locally_copy_models(model_type)
        model = TextEncoder(
            max_seq_lengths=MAX_SEQ_LENGTH,
            local_model_path=os.path.join(LOCAL_MODEL_DIR, model_type),
            local_preprocessor_path=os.path.join(LOCAL_MODEL_DIR, preprocessor),
            cluster="gcp",
            trainable=trainable,
            enable_dynamic_shapes=True,
        )
    return model


def get_loss(loss_name, from_logits, **kwargs):
    loss_name = loss_name.lower()
    if loss_name == "bce":
        print("Binary CE loss")
        return tf.keras.losses.BinaryCrossentropy(from_logits=from_logits)
    if loss_name == "cce":
        print("Categorical cross-entropy loss")
        return tf.keras.losses.CategoricalCrossentropy(from_logits=from_logits)
    if loss_name == "scce":
        print("Sparse categorical cross-entropy loss")
        return tf.keras.losses.SparseCategoricalCrossentropy(from_logits=from_logits)
    if loss_name == "focal_bce":
        gamma = kwargs.get("gamma", 2)
        print("Focal binary CE loss", gamma)
        return tf.keras.losses.BinaryFocalCrossentropy(gamma=gamma, from_logits=from_logits)
    if loss_name == "masked_bce":
        multit

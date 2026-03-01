# import tensorflow as tf
# from keras import layers

# @tf.keras.utils.register_keras_serializable()
# class FraudThreshold(layers.Layer):
#     def call(self, inputs):
#         return tf.cast(inputs >= 0.5, tf.int32)

# @tf.keras.utils.register_keras_serializable()
# class HighAmount(layers.Layer):
#     def call(self, x):
#         return tf.where(
#             x > 100000.0,
#             tf.fill(tf.shape(x), "High transaction amount"),
#             tf.fill(tf.shape(x), "")
#         )

# @tf.keras.utils.register_keras_serializable()
# class RiskyType(layers.Layer):
#     def call(self, x):
#         return tf.where(
#             tf.logical_or(
#                 tf.equal(x, "TRANSFER"),
#                 tf.equal(x, "CASH_OUT")
#             ),
#             tf.fill(tf.shape(x), "High-risk transaction type"),
#             tf.fill(tf.shape(x), "")
#         )

# @tf.keras.utils.register_keras_serializable()
# class ScoreText(layers.Layer):
#     def call(self, x):
#         score_str = tf.strings.as_string(x, precision=2)
#         return tf.strings.join(
#             ["Model risk score = ", score_str]
#         )

# @tf.keras.utils.register_keras_serializable()
# class JoinExplanation(layers.Layer):
#     def call(self, inputs):
#         return tf.strings.join(inputs, separator="; ")
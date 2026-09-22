import math
import re
import sys


class Calculator:
    def __init__(self):
        self.memory = 0.0
        self.history = []       # список (выражение, результат)
        self.angle_mode = "rad"  # "rad" или "deg"

    # ---------- вспомогательные функции для тригонометрии ----------

    def _to_rad(self, x):
        return math.radians(x) if self.angle_mode == "deg" else x

    def _from_rad(self, x):
        return math.degrees(x) if self.angle_mode == "deg" else x

    def sin(self, x):
        return math.sin(self._to_rad(x))

    def cos(self, x):
        return math.cos(self._to_rad(x))

    def tan(self, x):
        return math.tan(self._to_rad(x))

    def asin(self, x):
        return self._from_rad(math.asin(x))

    def acos(self, x):
        return self._from_rad(math.acos(x))

    def atan(self, x):
        return self._from_rad(math.atan(x))

    def factorial(self, x):
        return math.factorial(int(x))

    # ---------- перевод систем счисления ----------

    @staticmethod
    def to_bin(x):
        return bin(int(x))

    @staticmethod
    def to_oct(x):
        return oct(int(x))

    @staticmethod
    def to_hex(x):
        return hex(int(x))

    @staticmethod
    def to_dec(x):
        """Принимает строку вида '0b1010', '0o12', '0x0A' или обычное число."""
        s = str(x).strip()
        return int(s, 0)

    # ---------- безопасное вычисление выражений ----------

    def safe_eval(self, expr):
        """
        Вычисляет математическое выражение, разрешая только
        безопасный набор имён (без доступа к builtins).
        """
        expr = expr.strip()

        # поддержка "ans" — результат предыдущего вычисления
        if self.history:
            expr = re.sub(r"\bans\b", repr(self.history[-1][1]), expr)

        # разрешённые имена
        allowed_names = {
            "sqrt": math.sqrt,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
            "log": math.log,        # log(x, [base])
            "log10": math.log10,
            "log2": math.log2,
            "exp": math.exp,
            "factorial": self.factorial,
            "abs": abs,
            "round": round,
            "pow": pow,
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "bin": self.to_bin,
            "oct": self.to_oct,
            "hex": self.to_hex,
            "dec": self.to_dec,
        }
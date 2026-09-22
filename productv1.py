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
        # запрещаем двойное подчёркивание (защита от __import__ и т.п.)
        if "__" in expr:
            raise ValueError("Недопустимые символы в выражении")
 
        try:
            result = eval(expr, {"__builtins__": {}}, allowed_names)
        except ZeroDivisionError:
            raise ValueError("Деление на ноль")
        except (SyntaxError, TypeError, NameError) as e:
            raise ValueError(f"Некорректное выражение: {e}")
        return result
 
    # ---------- команды памяти ----------
 
    def handle_memory(self, cmd, current_value=None):
        cmd = cmd.upper()
        if cmd == "MC":
            self.memory = 0.0
            return "Память очищена"
        elif cmd == "MR":
            return f"Память: {self.memory}"
        elif cmd == "M+":
            if current_value is None:
                current_value = self.history[-1][1] if self.history else 0
            self.memory += current_value
            return f"Добавлено в память. Память: {self.memory}"
        elif cmd == "M-":
            if current_value is None:
                current_value = self.history[-1][1] if self.history else 0
            self.memory -= current_value
            return f"Вычтено из памяти. Память: {self.memory}"
        return None
 
 
HELP_TEXT = """
Доступные команды:
  <выражение>       вычислить (например: 2 + 2 * (3 - 1), sqrt(16), sin(pi/2))
  ans               результат предыдущего вычисления (можно использовать в выражении)
  M+ / M- / MR / MC команды памяти
  deg / rad         переключить режим углов для тригонометрии (сейчас: {mode})
  history           показать историю вычислений
  help              показать эту справку
  exit / quit       выйти
 
Функции: sqrt, sin, cos, tan, asin, acos, atan, log, log10, log2, exp,
         factorial, abs, round, pow
Константы: pi, e, tau
Системы счисления: bin(10), oct(10), hex(10), dec('0x1A')
"""
 
 
def main():
    calc = Calculator()
    print("=" * 50)
    print("   ЖЁСТКИЙ КАЛЬКУЛЯТОР")
    print("=" * 50)
    print(HELP_TEXT.format(mode=calc.angle_mode))
 
    while True:
        try:
            raw = input(f"[{calc.angle_mode}] >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока!")
            break
 
        if not raw:
            continue
 
        low = raw.lower()
 
        if low in ("exit", "quit", "q"):
            print("Пока!")
            break
 
        if low == "help":
            print(HELP_TEXT.format(mode=calc.angle_mode))
            continue
 
        if low == "history":
            if not calc.history:
                print("История пуста")
            else:
                for i, (expr, res) in enumerate(calc.history, 1):
                    print(f"  {i}. {expr} = {res}")
            continue
 
        if low == "deg":
            calc.angle_mode = "deg"
            print("Режим углов: градусы")
            continue
 
        if low == "rad":
            calc.angle_mode = "rad"
            print("Режим углов: радианы")
            continue
 
        if raw.upper() in ("M+", "M-", "MR", "MC"):
            print(calc.handle_memory(raw))
            continue
 
        try:
            result = calc.safe_eval(raw)
            calc.history.append((raw, result))
            print(f"= {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
if __name__ == "__main__":
    main()
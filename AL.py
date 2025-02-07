import re

TOKENS = [
    ("COMENTARIO", r"//[^\n]*|/\*(?:[^*]|\*(?!/)|/(?!\*))*\*/"),
    ("PALABRA_CLAVE", r"\b(if|else|int|float|string|while|return|true|false)\b"),
    ("IDENTIFICADOR", r"[a-zA-ZáéíóúÁÉÍÓÚñÑ_][a-zA-ZáéíóúÁÉÍÓÚñÑ0-9_]*"),
    ("NUMERO_FLOAT", r"-?\d*\.\d+|-?\d+\."),
    ("NUMERO", r"-?\d+"),
    ("LITERAL_CADENA", r'"(?:\\.|[^"\\])*"'),
    ("OPERADOR", r"[+\-*/=!]"),
    ("OPERADOR_LOGICO", r"&&|\|\|"),
    ("OPERADOR_COMPARACION", r"!==|===|==|!=|>=|<=|>|<"),
    ("DELIMITADOR", r"[;{}():]"),
    ("ESPACIO", r"[ \t\n]+")
]

def analizador_lexico(codigo_fuente):
    tokens = []
    pos = 0
    linea = 1
    
    while pos < len(codigo_fuente):
        match = None

        if pos > 0 and codigo_fuente[pos-1] == '\n':
            linea += 1

        if codigo_fuente[pos:pos+2] == '/*':
            cierre = codigo_fuente.find('*/', pos+2)
            if cierre == -1:
                raise ValueError(f"Error léxico: comentario multilínea sin cerrar en la posición {pos}")
        
        # Verificar identificadores inválidos
        if codigo_fuente[pos].isdigit():
            end = pos
            while end < len(codigo_fuente) and (codigo_fuente[end].isalnum() or codigo_fuente[end] == '_'):
                end += 1
            if end > pos and any(c.isalpha() for c in codigo_fuente[pos:end]):
                print(f"\nError en línea {linea}: Identificador inválido '{codigo_fuente[pos:end]}' - No puede comenzar con un número")

        if pos > 0 and codigo_fuente[pos] == '-':
            prev_char = codigo_fuente[pos-1]
            next_pos = pos + 1
            if (prev_char.isalnum() or prev_char == '_') and next_pos < len(codigo_fuente):
                next_char = codigo_fuente[next_pos]
                if next_char.isalnum() or next_char == '_':
                    print(f"\nError en línea {linea}: Identificador inválido - No se permiten guiones medios en identificadores")

        if pos > 0 and codigo_fuente[pos] == '-':
            prev_token = tokens[-1] if tokens else None
            if prev_token and prev_token[0] in ('NUMERO', 'NUMERO_FLOAT', 'IDENTIFICADOR'):
                tokens.append(('OPERADOR', '-'))
                pos += 1
                continue
                
        for token_tipo, patron in TOKENS:
            regex = re.compile(patron, re.DOTALL | re.UNICODE)
            match = regex.match(codigo_fuente, pos)
            
            if match:
                lexema = match.group(0)
                if token_tipo != "ESPACIO":
                    tokens.append((token_tipo, lexema))
                pos = match.end()
                break
                
        if not match:
            raise ValueError(f"Error léxico: carácter inesperado '{codigo_fuente[pos]}' en línea {linea}")
            
    return tokens

codigo_fuente = """
string señal = "México";
float año = 2024;
int días = 365;
"""

try:
    tokens = analizador_lexico(codigo_fuente)
    print("Tokens generados:")
    for token in tokens:
        print(token)
except ValueError as e:
    print(e)

#GEORFRANK VINCES
#ISMEL RODRIGUEZ
#-------------------------------------------------
import random
import time
import os
from colorama import init, Fore, Style
init(autoreset=True)


class Carta:
    def __init__(self, valor, palo):
        self._valor = valor
        self._palo = palo

    @property
    def valor_numerico(self):
        if self._valor in ['J', 'Q', 'K']: return 10
        if self._valor == 'A': return 11
        return int(self._valor)

    def imprimir(self):
        color = Fore.RED if self._palo in ['\u2665', '\u2666'] else Fore.WHITE
        print(color + "  _____")
        print(color + f" |{self._valor:<2}   |")
        print(color + f" |  {self._palo}  |")
        print(color + f" |___{self._valor:>2}|")
        print(Style.RESET_ALL, end="")

# clase baraja
class Baraja:
    def __init__(self, num_mazos=4):
        self._num_mazos = num_mazos
        self._cartas = []
        self.reiniciar()

    def reiniciar(self):
        palos = ['\u2660', '\u2665', '\u2666', '\u2663']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self._cartas = [Carta(v, p) for _ in range(self._num_mazos) for p in palos for v in valores]
        random.shuffle(self._cartas)

    def repartir(self):
        return self._cartas.pop() if self._cartas else None

# clase de participante :D
class Participante:
    def __init__(self):
        self.mano = []

    def calcular_puntuacion(self):
        puntos = sum(c.valor_numerico for c in self.mano)
        ases = sum(1 for c in self.mano if c._valor == 'A')
        while puntos > 21 and ases > 0:
            puntos -= 10
            ases -= 1
        return puntos

class Jugador(Participante):
    def __init__(self, saldo):
        super().__init__()
        self.saldo = saldo

class Crupier(Participante):
    pass

# clase controladora
class JuegoBlackJack:
    def __init__(self):
        self.baraja = Baraja(num_mazos=4)
        self.jugador = Jugador(1000)
        self.crupier = Crupier()
        self.apuesta_minima = 10

    def limpiar(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_mesa(self, apuesta, ocultar_crupier=True):
        self.limpiar()
        print(Fore.YELLOW + "=============================================")
        print(f"{Fore.GREEN} SU SALDO ES DE: ${self.jugador.saldo:<10} {Fore.CYAN} APUESTA: ${apuesta}")
        print(Fore.YELLOW + "=============================================")
        
        print(f"\n{Fore.MAGENTA} === MESA DEL CRUPIER ===")
        if ocultar_crupier:
            self.crupier.mano[0].imprimir()
            print(Fore.WHITE + "  [Carta Oculta]")
        else:
            for c in self.crupier.mano: c.imprimir()
            print(f"Puntaje Crupier: {self.crupier.calcular_puntuacion()}")
        
        print(f"\n{Fore.BLUE} === TUS CARTAS ===")
        for c in self.jugador.mano: c.imprimir()
        print(f"Tu Puntaje es de: {self.jugador.calcular_puntuacion()}")

    def iniciar(self):
        self.limpiar()
        print(Fore.CYAN + "="*45 + "\n    === WORLD BLACKJACK TOUR === POO EDITION :D -\n" + "="*45)
        self.jugador.saldo = int(input("Ingrese su saldo inicial: "))
        
        while self.jugador.saldo >= self.apuesta_minima:
            # Lógica de apuesta
            apuesta = int(input(f"\nDinero: ${self.jugador.saldo}. ¿Cuánto apuestas? (APUESTA TODO): "))
            self.jugador.mano = [self.baraja.repartir(), self.baraja.repartir()]
            self.crupier.mano = [self.baraja.repartir(), self.baraja.repartir()]
            
            # Blackjack Natural
            if self.jugador.calcular_puntuacion() == 21:
                print(Fore.GREEN + "¡¡¡BLACKJACK!!! Ganas 3 a 2. (pura suerte)")
                self.jugador.saldo += int(apuesta * 1.5)
            else:
                # Turno del Jugador
                while self.jugador.calcular_puntuacion() < 21:
                    self.mostrar_mesa(apuesta)
                    accion = input("\n[P]edir, [S]tand, [D]oblar, [R]endirse: ").upper()
                    if accion == 'P': self.jugador.mano.append(self.baraja.repartir())
                    elif accion == 'S': break
                    elif accion == 'D': 
                        apuesta *= 2; self.jugador.mano.append(self.baraja.repartir()); break
                    elif accion == 'R': self.jugador.saldo -= (apuesta // 2); break
                
                # Turno de Crupier
                while self.crupier.calcular_puntuacion() < 17:
                    self.crupier.mano.append(self.baraja.repartir())
                
                self.mostrar_mesa(apuesta, False)
                # Resolución finall
                pj, pc = self.jugador.calcular_puntuacion(), self.crupier.calcular_puntuacion()
                if pj > 21: print(Fore.RED + "¡TE PASASTE JAJA!"); self.jugador.saldo -= apuesta
                elif pc > 21 or pj > pc: print(Fore.GREEN + "¡GANASTE ESOOOO!"); self.jugador.saldo += apuesta
                elif pj < pc: print(Fore.RED + "LA CASA GANA :D"); self.jugador.saldo -= apuesta
                else: print("EMPATE.")

            if input("\n¿Otra ronda? (DI Q SI)(s/n): ").lower() != 's': break
        
        print(f"Juego terminado. Su saldo final :) ${self.jugador.saldo}")

if __name__ == "__main__":
    juego = JuegoBlackJack()
    juego.iniciar()
#include <stdio.h>

int main()
{
	int valor;
	int bandera = -1;
	int contador_error = 1;
	printf("\nIngrese el n�mero indicado para realizar la acci�n requerida:\n");
	printf("[1] Calcular �rea de un circulo.\n");
	printf("[2] Calcular volumen de una esfera.\n");
	printf("[3] Calcular volumen de un prisma circular.\n");
	printf("[4] Salir del programa.\n");
	while (bandera < 0)
	{
		printf("\nIngrese valor:\t");
		scanf("%d", &valor);
		if (valor == 1)
		{
			printf("El �rea de un c�culo con radio r=5 metros es %.2f. metros cuadrados.\n", 3.1416 * 5 * 5);
			bandera = valor;
		}
		else
		{
			if (valor == 2)
			{
				printf("Volumen de una esfera con radio r=5 metros es %.2f metros c�bicos.\n", ((float)4 / 3) * 3.1416 * 5 * 5 * 5);
				bandera = valor;
			}
			else
			{
				if (valor == 3)
				{
					printf("Volumen de un prisma circular con radio en la base de r=5 metros y altura h=10 metros es %.2f metros cúbicos.\n", 3.1416 * 5 * 5 * 10);
					bandera = valor;
				}
				else
				{
					if (valor == 4)
					{
						printf("El programa ha terminado.\n");
						bandera++;
					}
					else
					{
						if (contador_error < 3)
						{
							printf("Opci�n no v�lida, intente nuevamente.\n");
							contador_error++;
						}
						else
						{
							printf("El programa ha terminado.\n");
							bandera++;
						}
					}
				}
			}
		}
	}
	return 0;
}

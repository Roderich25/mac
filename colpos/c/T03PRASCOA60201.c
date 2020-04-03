#include <stdio.h>

int main()
{
	int n, anterior, actual, numero_incorrecto;
	char tipo;
	int orden = 0;
	int contador = 1;
	int posicion = -1;

	printf("Ingrese en tama�o de la lista: ");
	scanf("%d", &n);

	if (n <= 15)
	{
		if (n >= 5)
		{
			printf("Ingrese tipo de ordenamiento, A para ascendete o D para descendente: ");
			scanf("%s", &tipo);
			if (tipo == 'A')
			{
				orden = 1;
			}
			else
			{
				if (tipo == 'D')
				{
					orden = -1;
				}
			}
			if (orden != 0)
			{
				printf("Ingrese el primer valor: ");
				scanf("%d", &anterior);
				while (contador < n)
				{
					printf("Ingrese el siguiente valor: ");
					scanf("%d", &actual);
					if (orden > 0)
					{
						if (anterior > actual)
						{
							if (posicion == -1)
							{
								posicion = contador + 1;
								numero_incorrecto = actual;
							}
						}
					}
					else
					{
						if (anterior < actual)
						{
							if (posicion == -1)
							{
								posicion = contador + 1;
								numero_incorrecto = actual;
							}
						}
					}
					contador++;
					anterior = actual;
				}
				if (posicion == -1)
				{
					printf("\tOrdenamiento correcto!\n");
				}
				else
				{
					printf("\tEl n�mero %d es incorrecto en la posici�n %d.\n", numero_incorrecto, posicion);
				}
			}
			else
			{
				printf("Orden requerido inv�lido!\n");
			}
		}
		else
		{
			printf("Tama�o de lista no v�lido. Muy peque�o!\n");
		}
	}
	else
	{
		printf("Tama�o de lista no v�lido. Muy grande!\n");
	}
	return 0;
}

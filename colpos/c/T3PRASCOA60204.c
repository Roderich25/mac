#include <stdio.h>

int main()
{
	int hileras;
	int columnas;
	printf("Ingresar n�mero de hileras:\t");
	scanf("%d", &hileras);
	printf("Ingresar n�mero de columnas:\t");
	scanf("%d", &columnas);

	if (hileras >= 4)
	{
		if (hileras <= 10)
		{
			if (columnas >= 12)
			{
				if (columnas <= 20)
				{
					int i;
					for (i = 0; i < hileras; i++)
					{
						int j;
						for (j = 0; j < columnas; j++)
						{
							if (columnas % 2)
							{
								printf("%3d", columnas - j);
							}
							else
							{
								printf("%3d", j + 1);
							}
						}
						printf("\n");
						--columnas;
					}
				}
				else
				{
					printf("El n�mero m�ximo de columnas es 20");
				}
			}
			else
			{
				printf("El n�mero m�nimo de columnas es 12.");
			}
		}
		else
		{
			printf("El n�mero m�ximo de hileras es 10.\n");
		}
	}
	else
	{
		printf("El n�mero m�nimo de hileras es 4.\n");
	}
	return 0;
}

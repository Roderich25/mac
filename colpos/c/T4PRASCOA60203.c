#include <stdio.h>

int main()
{
    int primero, segundo, tercero, cuarto, quinto, temporal;
    int bandera = 0;
    printf("Ingresar 5 n�meros enteros positivos.\n");
    printf("Ingresar primer entero positivo:\t");
    scanf("%d", &primero);
    printf("Ingresar segundo entero positivo:\t");
    scanf("%d", &segundo);
    if (segundo < primero)
    {
        temporal = primero;
        primero = segundo;
        segundo = temporal;
    }
    printf("Ingresar tercer entero positivo:\t");
    scanf("%d", &tercero);
    if (tercero < segundo)
    {
        temporal = segundo;
        segundo = tercero;
        tercero = temporal;
        if (segundo < primero)
        {
            temporal = primero;
            primero = segundo;
            segundo = temporal;
        }
    }
    printf("Ingresar cuarto entero positivo:\t");
    scanf("%d", &cuarto);
    if (cuarto < tercero)
    {
        temporal = tercero;
        tercero = cuarto;
        cuarto = temporal;
        if (tercero < segundo)
        {
            temporal = segundo;
            segundo = tercero;
            tercero = temporal;
            if (segundo < primero)
            {
                temporal = primero;
                primero = segundo;
                segundo = temporal;
            }
        }
    }
    printf("Ingresar quinto entero positivo:\t");
    scanf("%d", &quinto);
    if (quinto < cuarto)
    {
        temporal = cuarto;
        cuarto = quinto;
        quinto = temporal;
        if (cuarto < tercero)
        {
            temporal = tercero;
            tercero = cuarto;
            cuarto = temporal;
            if (tercero < segundo)
            {
                temporal = segundo;
                segundo = tercero;
                tercero = temporal;
                if (segundo < primero)
                {
                    temporal = primero;
                    primero = segundo;
                    segundo = temporal;
                }
            }
        }
    }
    do
    {
        printf("Ingresar el c�lculo requerido para la lista suministrada:\n");
        printf("[1] m�ximo\n");
        printf("[2] m�nimo\n");
        printf("[3] mediana\n> ");
        scanf("\t%d", &bandera);
        switch(bandera){
        	case 1:
        		printf("El m�ximo de la lista es: %d.\n", quinto);
        		break;
        	case 2:
        		printf("El m�nimo de la lista es: %d.\n", primero);
        		break;
        	case 3:
        		printf("La mediana de la lista es: %d.\n", tercero);
        		break;
        	default:
        		printf("Opci�n no v�lida.\n");
				break;		
		}
        printf("Para realizar otro c�culo con la misma lista presione [1], para salir ingresar cualquier tecla distinta de [1]:\t");
        scanf("%d", &bandera);
        if (!(bandera == 1))
            bandera = -1;

    } while (bandera >= 0);
    printf("\nEl programa ha terminado.\n");
    return 0;
}

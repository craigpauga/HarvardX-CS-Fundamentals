#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    //Open Memory Card
    FILE *file = fopen("card.raw", "r");

    //Check if memory card cannot be found
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;

    //Integer to label imgs
    int jpeg_count = 0;
    //Search Memory Card
    while (fread(buffer, BLOCK_SIZE, 1, file))
    {


        //Find beginning of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", jpeg_count);
            jpeg_count++;
            img = fopen(filename, "w");
        }

        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }


    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);

    return 0;
}

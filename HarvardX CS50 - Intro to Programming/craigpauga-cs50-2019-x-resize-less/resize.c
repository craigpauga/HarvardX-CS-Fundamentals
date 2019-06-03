// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "bmp.h"

int main(int argc, char *argv[])
{

    // ensure proper usage
    if (argc != 4)
    {

        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    //Ensure that argv[1] can't be more than 3 digits
    if (strlen(argv[1]) > 3)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    //Ensure that argv[1] is stricly numerical
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (argv[1][i] < '0' || argv[1][i] > '9')
        {
            fprintf(stderr, "Usage: resize n infile outfile\n");
            return 1;
        }
    }

    int n = atoi(argv[1]);

    if (n < 1 || n > 100)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfL;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfL = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biL;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biL = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }


    //Modify BITMAPINFOHEADER
    biL.biHeight = n * bi.biHeight;
    biL.biWidth = n * bi.biWidth;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_L = (4 - (biL.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    biL.biSizeImage = (abs(biL.biWidth) * abs(biL.biHeight) * sizeof(RGBTRIPLE)) + (padding_L * abs(biL.biHeight));

    //Modify BITMAPFILE HEADER
    bfL.bfSize = bf.bfSize - bi.biSizeImage + biL.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfL, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biL, sizeof(BITMAPINFOHEADER), 1, outptr);



    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int y = 0; y < n; y++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int x = 0; x < n; x++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }


            // then add it back (to demonstrate how)
            for (int k = 0; k < padding_L; k++)
            {
                fputc(0x00, outptr);
            }

            if (y < n - 1)
            {
                fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

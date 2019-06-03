//Craig Pauga
//CS50 May 2019

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 100

//Represent word count
int word_count = 0;

// Represents a hash table
node *hashtable[N];

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {

        //Allocate space for word
        node *n = malloc(sizeof(node));

        //Check for segmentation fault
        if(!n)
        {
            return NULL;
        }


        //Call hash function
        int key = hash((unsigned char *) word);

        //Get head of linked list
        node *head = hashtable[key];

        //Add word to list
        strcpy(n->word,word);

        //Update Pointer
        n->next = NULL;


        //If bucket empty, add node
        if (head == NULL)
        {
            hashtable[key] = n;
        }
        else
        {
            n->next = hashtable[key];
            hashtable[key] = n;
        }

        word_count++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    //Make buffer for word
    char buffer[LENGTH];

    //Copy word
    strcpy(buffer,word);

    //Length of word
    int l = strlen(word);

    //Make everything from the text lowercase
    for (int i = 0; i < l; i++)
    {
        buffer[i] = tolower(word[i]);
    }

    //Get hash of word
    int key = hash((unsigned char *) buffer);

    //Navigate the list starting from the head
    node *cur_node = hashtable[key];

    //Check the linked list for match string
    while (cur_node != NULL)
    {
        if (strcmp(cur_node->word,buffer) == 0)
        {
            //Word has been found
            return true;
        }
        else
        {
            //Check next pointer
            cur_node = cur_node->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    //Iterate through each hash bucket
    for (int hash = 0; hash < N; hash++)
    {
        //Create head node
        node *ptr = hashtable[hash];

        //Unload each node until pointer is null
        while (ptr != NULL)
        {
            node *n = ptr;
            ptr = ptr->next;
            free(n);
        }

    }

    return true;
}


// djb2 hash function source: http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(unsigned char *str)
{
    //Large hash
    unsigned long hash = 5381;

    //Initilalize
    int c;

    //Loop over each char
    while ((c = *str++))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    hash = hash % N;
    return hash;
}
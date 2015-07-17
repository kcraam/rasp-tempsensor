CC = gcc
CFLAGS =  -std=c99 -I. -lbcm2835
DEPS = 
OBJ = tempsensor.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

tempsensor: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)

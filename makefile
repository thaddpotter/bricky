CC=gcc

INCLUDE_FLAGS= -I. -lm
WARNING_FLAGS=-Wall -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations
CFLAGS = $(INCLUDE_FLAGS) $(WARNING_FLAGS)

all: 
	$(CC) -o brick.out ./brick.c $(CFLAGS)

easy:
	$(CC) -o brick.out ./brick.c -I.

clean:
	rm -rf ./*.out
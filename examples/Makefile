

BW64_READ_O = bw64_read.o
BW64_READ = bw64_read

CFLAGS = -Wall
LIBS = -lsndfile
INCLUDE = -I../src -I../src/GSM610

TARGET = bw64_read

.SUFFIXES: .c

.c.o:
	gcc $(CFLAGS) $(INCLUDE) -c $<


default: all

all: $(BW64_READ)

$(BW64_READ): $(BW64_READ_O)
	gcc $(CFLAGS) $(LIBS) $(BW64_READ_O) -o $(BW64_READ)

clean:
	rm -f *.o *~

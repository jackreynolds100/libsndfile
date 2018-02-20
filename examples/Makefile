

BW64_READ_O = bw64_read.o
MAKE_SINE_CHNA_BW64_O = make_sine_chna_BW64.o
BW64_READ = bw64_read
MAKE_SINE_CHNA_BW64 = make_sine_chna_BW64

CFLAGS = -Wall
LIBS = -lsndfile
INCLUDE = -I../src -I../src/GSM610

#TARGET = bw64_read

.SUFFIXES: .c

.c.o:
	gcc $(CFLAGS) $(INCLUDE) -c $<


default: all

all: $(BW64_READ) $(MAKE_SINE_CHNA_BW64)

$(BW64_READ): $(BW64_READ_O)
	gcc $(CFLAGS) $(LIBS) $(BW64_READ_O) -o $(BW64_READ)

$(MAKE_SINE_CHNA_BW64): $(MAKE_SINE_CHNA_BW64_O)
	gcc $(CFLAGS) $(LIBS) $(MAKE_SINE_CHNA_BW64_O) -o $(MAKE_SINE_CHNA_BW64)

clean:
	rm -f *.o *~

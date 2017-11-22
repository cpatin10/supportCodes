#ifndef __SIMPLESEMAPHORE_H_
#include "SimpleSemaphore.h"
#define __SIMPLESEMAPHORE_H_
#endif

#ifndef __SHAREDMEMORY_H_
#include "SharedMemory.h"
#define __SHAREDMEMORY_H_
#endif

#ifndef __IOSTREAM__
#include <iostream>
#define __IOSTREAM__
#endif


int main() {
  SimpleSemaphore sem1("/sem-empty",1);
  SimpleSemaphore sem2("/sem-full",0);
  SharedMemory<int> sm("/mem");
  int &i = sm();
  int producto;

  while(true) {
    cout << "Esperando por el Wait" << endl;
    sem2.Wait();
    producto = i;
    sem1.Signal();
    cout << "Consumiento producto " << producto << endl;
    sleep(2);
    cout << "Terminé" << endl;
  }
        
  return 0;
}

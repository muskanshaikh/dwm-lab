import numpy as np
N = int(input("Number Of Pages:"))
d=0.85
eps=1.0e-8
print("\n please enter the adjanecey matrix for the network")
print("\n Type 1 if there is a link from a page i to page j else type 0" )
links = []
for i in range(0,N):
  L=[]
  for j in range(0,N):
    L.append(int(input('Page '+str(i+1)+'to page' +str(j+1)+': ')))
  links.append(L)

outBoundL = np.zeros((N,),dtype=int)

for i in range(0,N):
  for j in range(0,N):
    if links[i][j]==1:
      outBoundL[i]=outBoundL[i]+1

M = np.zeros((N,N))
for i in range(0,N):
  for j in range(0,N):
    if links[j][i]==1:
      M[i][j]=1/outBoundL[j]

M = np.matrix(M)
onecolmat=np.matrix(np.ones((N,1),dtype=int))

R= np.matrix(np.full((N,1),1/N))

while True:
  Rnext=d*np.dot(M,R)+((1-d)/N)*onecolmat
  diff=np.subtract(Rnext,R)
  if np.linalg.norm(diff)<eps:
    break
  R=Rnext
  
print(Rnext)
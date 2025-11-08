import math


"""
   Lost = ((2^BitsFAT) - (((ArmazenamentoTotalGB * 1024^3 / BytesPorSetor) - (1 + 18 + 2 * (2^BitsFAT * BitsFAT/8)/bytesPorSetor))/ SetorPorCluster))*8



"""

def Perda(BitsFAT, ArmazenamentoTotalGB, BytesPorSetor, SetorPorCluster):

    SetoresBootRecord = 1

    SetoresRootDir = 18

    # Tamanho total em bytes de DUAS tabelas FAT
    TamanhoFAT_Bytes = 2 * (2**BitsFAT * (BitsFAT / 8))

    # Usar ceil para arredondar para cima já que não da para ocupar setor pela metade
    SetoresFAT = math.ceil(TamanhoFAT_Bytes / BytesPorSetor)

    # Número de setores que sobraram para a área de dados
    # A função floor é para truncar a saida já que não da pra usar setor pela metade
    SetoresDados = math.floor((ArmazenamentoTotalGB * 1024**3 / BytesPorSetor) - \
        (SetoresBootRecord + SetoresRootDir + 2 * SetoresFAT))
    
    # Número de Clusters endereçaveis pela FAT
    NumClusterEnderecaveis = 2**BitsFAT

    # Número de Clusters possíveis na área de dados
    NumClustersPossiveis = math.floor(SetoresDados / SetorPorCluster)

    # Clusters que não serão endereçados (perda)
    EnderecosNaoUtilizadosFAT = (NumClusterEnderecaveis - NumClustersPossiveis)

    # Tamanho endereço FAT em bytes
    TamanhoEnderecoFAT = BitsFAT / 8

    BytesNaoUtilizadosFAT = EnderecosNaoUtilizadosFAT * TamanhoEnderecoFAT
    
    
    ######## Espaço Vazio no Final da Área de dados #######

    NumClusterNaoUtilizadosDados = NumClustersPossiveis - NumClusterEnderecaveis

    EspacoVazioDados = NumClusterNaoUtilizadosDados * SetorPorCluster * BytesPorSetor

    # Se EspacoVazioDados é negativo, quer dizer que todos os clusters são endereçaveis
    # para a quantidade de bits escolhida
    if EspacoVazioDados < 0: 
        EspacoVazioDados = 0

    if BytesNaoUtilizadosFAT < 0: 
        BytesNaoUtilizadosFAT = 0    

    # Perda em bytes
    Perda = BytesNaoUtilizadosFAT + EspacoVazioDados

    return Perda


def main():

    # Parametros
    ArmazenamentoTotalGB = 64

    # Testará todos as possibilidades para quantidade de bits da FAT entre 1 e 64
    BitsFAT_possiveis = [i for i in range(1,65)]
    
    # Testará todas as possibilidades entre 128 até 8096 bytes por setor
    BytesPorSetor_possiveis = [2**i for i in range(7,14)]

    # Testará todas as possibilidades entre 1 até 16 setores por cluster
    SetorPorCluster_possiveis = [i for i in range(1,17)]

    
    
    menor_perda = 99999999999
    parametros_menor_perda = []

    for BitsFAT in BitsFAT_possiveis:
        for BytesPorSetor in BytesPorSetor_possiveis:
            for SetorPorCluster in SetorPorCluster_possiveis:
                
                perda_atual = Perda(BitsFAT, ArmazenamentoTotalGB, BytesPorSetor, SetorPorCluster)

                if perda_atual < menor_perda:
                    menor_perda = perda_atual
                    parametros_menor_perda = [ArmazenamentoTotalGB, BitsFAT, BytesPorSetor, SetorPorCluster]


    print(f"A menor perda para um armazenamento total de {parametros_menor_perda[0]} GB foi de {menor_perda} bytes\n")
    print("Parâmatros:")
    print(f"bits para FAT: {parametros_menor_perda[1]}")
    print(f"Bytes por setor: {parametros_menor_perda[2]}")
    print(f"Setores por cluster: {parametros_menor_perda[3]}")


if __name__ == "__main__":
    main()
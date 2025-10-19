import sys, os
sys.path.insert(0, os.path.abspath('.'))
from data.usuario import usuario_repo

if __name__ == '__main__':
    print('Executando backfill de registros de tipo...')
    usuario_repo.backfill_registros_tipo()
    print('Backfill finalizado.')

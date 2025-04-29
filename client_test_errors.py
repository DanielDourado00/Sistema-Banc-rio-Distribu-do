import grpc
import bank_pb2
import bank_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bank_pb2_grpc.BankServiceStub(channel)

        print("\n Teste 1: Consultar saldo de conta inexistente")
        try:
            response = stub.GetBalance(bank_pb2.AccountRequest(account_id="nonexistent_account"))
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")

        print("\n Teste 2: Fazer depósito com valor negativo")
        try:
            response = stub.Deposit(bank_pb2.DepositRequest(account_id="123", amount=-50.0))
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")

        print("\n Teste 3: Fazer saque com valor negativo")
        try:
            response = stub.Withdraw(bank_pb2.WithdrawRequest(account_id="123", amount=-30.0))
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")

        print("\n Teste 4: Tentar sacar valor maior que o saldo disponível")
        try:
            response = stub.Withdraw(bank_pb2.WithdrawRequest(account_id="123", amount=1000000.0))
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")

        print("\n Teste 5: Tentar aplicar juros negativos")
        try:
            response = stub.CalculateInterest(bank_pb2.InterestRequest(account_id="123", annual_interest_rate=-5.0))
        except grpc.RpcError as e:
            print(f"[{e.code().name}] {e.details()}")

if __name__ == '__main__':
    main()

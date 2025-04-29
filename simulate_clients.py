import grpc
import threading
import bank_pb2
import bank_pb2_grpc

def simulate_client(client_id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bank_pb2_grpc.BankServiceStub(channel)
        account_id = f"user_{client_id}"

        try:
            # Criar uma nova conta para o cliente
            stub.CreateAccount(bank_pb2.AccountRequest(account_id=account_id, account_type="savings"))
            print(f"[Client {client_id}] Account created.")

            # Depositar 100.0
            stub.Deposit(bank_pb2.DepositRequest(account_id=account_id, amount=100.0))
            print(f"[Client {client_id}] Deposited 100.0.")

            # Sacar 20.0
            stub.Withdraw(bank_pb2.WithdrawRequest(account_id=account_id, amount=20.0))
            print(f"[Client {client_id}] Withdrew 20.0.")

            # Ver saldo final
            response = stub.GetBalance(bank_pb2.AccountRequest(account_id=account_id))
            print(f"[Client {client_id}] Final balance: {response.balance}")

        except grpc.RpcError as e:
            print(f"[Client {client_id}] Error: [{e.code().name}] {e.details()}")

def main():
    threads = []
    number_of_clients = 20  # Você pode mudar para 10, 50, 100 clientes!

    for i in range(number_of_clients):
        t = threading.Thread(target=simulate_client, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

import grpc
import bank_pb2
import bank_pb2_grpc

def create_account(stub, account_id, account_type):
    request = bank_pb2.AccountRequest(account_id=account_id, account_type=account_type)
    response = stub.CreateAccount(request)
    print(response.message)

def get_balance(stub, account_id):
    try:
        request = bank_pb2.AccountRequest(account_id=account_id)
        response = stub.GetBalance(request)
        print(f"Balance: {response.balance}")
    except grpc.RpcError as e:
        print(f"[{e.code().name}] {e.details()}")

def deposit(stub, account_id, amount):
    try:
        request = bank_pb2.DepositRequest(account_id=account_id, amount=amount)
        response = stub.Deposit(request)
        print(response.message)
    except grpc.RpcError as e:
        print(f"[{e.code().name}] {e.details()}")

def withdraw(stub, account_id, amount):
    try:
        request = bank_pb2.WithdrawRequest(account_id=account_id, amount=amount)
        response = stub.Withdraw(request)
        print(response.message)
    except grpc.RpcError as e:
        print(f"[{e.code().name}] {e.details()}")

def calculate_interest(stub, account_id, rate):
    try:
        request = bank_pb2.InterestRequest(account_id=account_id, annual_interest_rate=rate)
        response = stub.CalculateInterest(request)
        print(response.message)
    except grpc.RpcError as e:
        print(f"[{e.code().name}] {e.details()}")

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bank_pb2_grpc.BankServiceStub(channel)

        # Exemplos de uso:
        create_account(stub, "123", "savings")
        deposit(stub, "123", 100.0)
        withdraw(stub, "123", 30.0)
        get_balance(stub, "123")
        calculate_interest(stub, "123", 10)

if __name__ == '__main__':
    main()

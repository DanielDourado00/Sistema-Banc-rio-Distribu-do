import grpc
from concurrent import futures
import redis
import bank_pb2
import bank_pb2_grpc

class BankService(bank_pb2_grpc.BankServiceServicer):
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def CreateAccount(self, request, context):
        if self.redis.exists(request.account_id):
            return bank_pb2.AccountResponse(message="Account already exists.")
        self.redis.hset(request.account_id, mapping={
            "account_type": request.account_type,
            "balance": 0.0
        })
        return bank_pb2.AccountResponse(message="Account created successfully.")

    def GetBalance(self, request, context):
        if not self.redis.exists(request.account_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found. Please check the account ID.")
        balance = float(self.redis.hget(request.account_id, "balance"))
        return bank_pb2.BalanceResponse(balance=balance)

    def Deposit(self, request, context):
        if request.amount <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Transaction amount must be positive.")
        if not self.redis.exists(request.account_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found. Please check the account ID.")
        self.redis.hincrbyfloat(request.account_id, "balance", request.amount)
        return bank_pb2.TransactionResponse(message="Deposit successful.")

    def Withdraw(self, request, context):
        if request.amount <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Transaction amount must be positive.")
        if not self.redis.exists(request.account_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found. Please check the account ID.")
        current_balance = float(self.redis.hget(request.account_id, "balance"))
        if current_balance < request.amount:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Insufficient funds for the requested withdrawal.")
        self.redis.hincrbyfloat(request.account_id, "balance", -request.amount)
        return bank_pb2.TransactionResponse(message="Withdrawal successful.")

    def CalculateInterest(self, request, context):
        if request.annual_interest_rate <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Annual interest rate must be a positive value.")
        if not self.redis.exists(request.account_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Account not found. Please check the account ID.")
        balance = float(self.redis.hget(request.account_id, "balance"))
        interest = balance * (request.annual_interest_rate / 100)
        self.redis.hincrbyfloat(request.account_id, "balance", interest)
        return bank_pb2.TransactionResponse(account_id=request.account_id, message=f"Interest of {interest:.2f} applied.", balance=balance + interest)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

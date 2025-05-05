function Home() {
  return (
    <div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <h1 className="text-center mb-3">Welcome Corey!</h1>

        <p className="text-center mb-1">
          Orders are in the list of Alpaca. You can see the table in Orders
          Page, check the status of every Orders
        </p>
        <p className="text-center mb-1">
          Webhooks Page is for All signals from TradingView, for now it works
          with manual Webhooks.
        </p>
      </div>
    </div>
  );
}

export default Home;

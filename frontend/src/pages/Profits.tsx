import Table, { Column } from "../components/Table";
import { useEffect, useState } from "react";
import axios from "axios";

type LogType = {
  ticker: string;
  action: string;
  quantity: number;
  price: number;
  date: string;
  type: string;
  status: string;
  limitPrice: number;
  position_intent: string;
  profit?: number; // Optional profit field
};

const columns: Column<LogType>[] = [
  { key: "ticker", label: "Ticker", sortable: true },
  { key: "action", label: "Action", sortable: true },
  { key: "quantity", label: "Quantity", sortable: true },
  { key: "type", label: "Type", sortable: true },
  { key: "limitPrice", label: "Limit Price", sortable: true },
  { key: "status", label: "Status" },
  { key: "date", label: "Date", sortable: true },
  // { key: "position_intent", label: "Position Intent" },
  { key: "profit", label: "Profit", sortable: true }, // Added profit column
];

function Profits() {
  const [logs, setLogs] = useState<LogType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const response = await axios.get<LogType[]>(
        "http://localhost:8000/api/orders/live"
      );
      let data = response.data;
      data = data.filter((log) => log.status === "filled");
      let profits = calcProfits(data);
      setLogs(profits);
      setError(null);
    } catch (err) {
      setError("Failed to fetch orders");
    } finally {
      setLoading(false);
    }
  };

  const calcProfits = (logs: LogType[]): LogType[] => {
    let reorderedLogs: LogType[] = logs;
    // reorderedLogs = logs.sort((a, b) => {
    //   return new Date(a.date).getTime() - new Date(b.date).getTime();
    // });
    let curprice: { [key: string]: number } = {};
    let curcount: { [key: string]: number } = {};
    for (let i = reorderedLogs.length - 1; i >= 0; i --) {
      let ticker = reorderedLogs[i].ticker;
      let action = reorderedLogs[i].action;
      let quantity = Number(reorderedLogs[i].quantity) || 0;
      let price = Number(reorderedLogs[i].limitPrice) || 0;
      if (curcount[ticker] === undefined) curcount[ticker] = 0;
      if (curprice[ticker] === undefined) curprice[ticker] = 0;
      console.log(
        action,
        ticker,
        quantity,
        price,
        curprice[ticker],
        curcount[ticker]
      );
      if (quantity === 0) continue;
      if (action === "buy") {
        curprice[ticker] =
          (price * quantity + curprice[ticker] * curcount[ticker]) /
          (quantity + curcount[ticker]);

        curcount[ticker] = quantity + curcount[ticker];
        reorderedLogs[i].profit = 0;
        // console.log(curprice[ticker]);
      } else if (action === "sell") {
        let profit = (price - curprice[ticker]) * quantity;
        profit = Math.round(profit * 100) / 100;
        curcount[ticker] = curcount[ticker] - quantity;
        reorderedLogs[i].profit = profit;
        if (curcount[ticker] === 0) {
          delete curprice[ticker];
          delete curcount[ticker];
        }
      }
    }
    return reorderedLogs;
  };

  useEffect(() => {
    fetchLogs();
    // const interval = setInterval(fetchLogs, 10000); // Auto-refresh every 10 seconds
    // return () => clearInterval(interval); // Cleanup on unmount
  }, []);
  return (
    <div className="w-full min-h-screen pt-10">
      {loading && <div className="text-center">Loading...</div>}
      {error && <div className="text-red-500 text-center">{error}</div>}
      {!loading && !error && (
        <div className="max-w-6xl mx-auto bg-white shadow-lg rounded-lg">
          <Table columns={columns} data={logs} />
        </div>
      )}
    </div>
  );
}

export default Profits;

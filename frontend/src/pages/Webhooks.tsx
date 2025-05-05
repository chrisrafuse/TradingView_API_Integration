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
  status: "failed" | "polling" | "filled" | "expiry";
  limitPrice: number;
  // order_id: string;
  message: string;
};

const columns: Column<LogType>[] = [
  { key: "ticker", label: "Ticker", sortable: true },
  { key: "action", label: "Action", sortable: true },
  { key: "quantity", label: "Quantity", sortable: true },
  { key: "price", label: "Price", sortable: true },  
  { key: "date", label: "Date", sortable: true },  
  { key: "status", label: "Status", sortable: true },
  { key: "limitPrice", label: "Limit Price", sortable: true },  
  // { key: "order_id", label: "OrderId", sortable: true },
  { key: "message", label: "Message", sortable: true }, 
];

function Webhooks() {
  const [logs, setLogs] = useState<LogType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const response = await axios.get<LogType[]>(
        "/api/webhooks/db"
      );
      console.log(response.data);
      let data = response.data.sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      })
      setLogs(data);
      // setLogs(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch webhooks");
    } finally {
      setLoading(false);
    }
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

export default Webhooks;

import Table, { Column } from "../components/Table";
import { useEffect, useState } from "react";
import axios from "axios";

type LogType = {
  symbol: string;
  side: string;
  qty: number;
  cost_basis: number;
  market_value: string;
  current_price: string;
 
};

const columns: Column<LogType>[] = [
  { key: "symbol", label: "Symbol", sortable: true },
  { key: "side", label: "Side", sortable: true },
  { key: "qty", label: "Quantity", sortable: true },
//   { key: "cost_basis", label: "CostBasis", sortable: true },
  { key: "market_value", label: "Market Value", sortable: true },
  { key: "current_price", label: "Current Price" },
];

function Positions() {
  const [logs, setLogs] = useState<LogType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const response = await axios.get<LogType[]>(
        "/api/positions/live"
      );
      setLogs(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch positions");
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

export default Positions;

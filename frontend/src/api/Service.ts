const url: string = "https://127.0.0.1:3001/";

export default class APIService {
  static async GetData(route: string): Promise<any> {
    try {
      const response: Response = await fetch(url.concat(route), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Accept: "application/json",
        },
      });

      return await response.json();
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  static async PostData(route: string, body: any): Promise<any> {
    try {
      const response: Response = await fetch(url.concat(route), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Accept: "application/json",
        },
        body: JSON.stringify(body),
      });

      return await response.json();
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

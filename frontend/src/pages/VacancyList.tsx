import axios from "axios";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Page() {
  const vacancies1 = [
    { id: 1, title: "Продавец", salary: 5000 },
    { id: 2, title: "Разносчик", salary: 2000 },
    { id: 3, title: "Повар", salary: 3000 },
  ];
  const [getterVacansies, setterVacansies] = useState([]);

  async function getAllVacansies() {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/vacansies/list"
    );
    if (response.status === 200) {
      console.log(response.data);

      setterVacansies(response.data);
    } else {
      console.log(response.status);
    }
  }

  async function deleteVacancy(id: number) {
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/vacansies/delete/${id}/`
    );
    if (response.status === 200) {
      getAllVacansies();
    } else {
      console.log(response.status);
    }
  }

  useEffect(() => {
    getAllVacansies();
  }, []);

  return (
    <div>
      <div className={"input-group"}>
        <Link className={"btn btn-lg btn-outline-primary"} to={"/"}>
          все вакансии
        </Link>
        <Link className={"btn btn-lg btn-outline-success"} to={"/create"}>
          опубликовать вакансию
        </Link>
      </div>
      <h1>Список вакансий!</h1>
      <div className={"row row-cols-3"}>
        {getterVacansies && getterVacansies.length > 0 ? (
          getterVacansies.map((item, index) => (
            <div className={"card col-2"}>
              <Link
                // @ts-ignore
                to={`/${item.id}`}
                className={"text-decoration-none text-dark"}
              >
                <div className={"lead"}>
                  {
                    // @ts-ignore
                    item.title
                  }
                </div>
                (
                {
                  // @ts-ignore
                  item.salary
                }
                )
              </Link>
              <button
                onClick={
                  // @ts-ignore
                  () => deleteVacancy(item.id)
                }
              >
                удалить
              </button>
            </div>
          ))
        ) : (
          <div>Данных пока нет!</div>
        )}
      </div>
    </div>
  );
}

import React from 'react'

const PastPage = () => {
  return (
    <div className='main h-96 border-solid border-[1px] border-[#ebebeb]'>
      <div className="m-5 ">
        <div className="flex items-center gap-5">
          <img src="" alt="Пользователь" />
          <p>Title</p>
        </div>
        
        <div className="flex gap-4 items-center">
          <div className="flex gap-2 items-center">
            <img src="" alt="Пользователь" />
            <p>User</p>
          </div>
          <div className="flex gap-2 items-center">
            <img src="" alt="Дата" />
            <p>Date</p>
          </div>
          <div className="flex gap-2 items-center">
            <img src="" alt="Кол-во просмотров" />
            <p>View</p>
          </div>
          <div className="flex gap-2 items-center">
            <img src="" alt="Таймер"/>
            <p>Time delete</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PastPage
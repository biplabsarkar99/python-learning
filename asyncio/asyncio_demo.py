import asyncio as aio

async def find_divisibles(irange,divisor):
    nums= []
    print ("Finding nums in range {} divisible by {}.".format(irange,divisor))
    for num in range(irange):
        if (num%divisor==0):
            nums.append(num)
    print ("Done finding divisibles in range {} divisible by {}.".format(irange,divisor))
    return nums

async def main():
    div1 = loop.create_task(find_divisibles(50000099999531,341))
    div2 = loop.create_task(find_divisibles(8100009999999521300,499))
    div3 = loop.create_task(find_divisibles(98600, 799))
    div4 = loop.create_task(find_divisibles(8100009999999521300, 8771))
    div5 = loop.create_task(find_divisibles(810099999992229009999999521300999723, 499887))
    await aio.wait([div1,div2,div3,div4,div5]) #Runs Synchronously , waits for completion of ech task

if __name__=='__main__':
    try:
        loop = aio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as ex:
        pass
    finally:
        loop.close()
